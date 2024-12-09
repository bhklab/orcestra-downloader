# %% imports
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime
import difflib
import aiohttp
import asyncio
from rich.progress import Progress
from pathlib import Path
import json
from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
log = logging.getLogger("orcestra")

# %% Cache
CACHE_DIR = Path.home() / ".cache/orcestradownloader"
CACHE_FILE = CACHE_DIR / "psets.json"

CACHE_DAYS_TO_KEEP = 7

def get_cached_response() -> Optional[List[dict]]:
    """Retrieve cached response if it exists and is up-to-date."""
    log.debug("Checking for cached response...")
    if not CACHE_FILE.exists():
        log.info("Cache file not found.")
        return None
    try:
        with CACHE_FILE.open("r") as f:
            cached_data = json.load(f)
        cache_date = datetime.fromisoformat(cached_data["date"])
        # Check if the cache is still valid
        if (datetime.now() - cache_date).days <= CACHE_DAYS_TO_KEEP:
            diff = datetime.now() - cache_date
            if diff.days > 0:
                daysago = f"{diff.days} days ago"
            else:
                minutes = diff.seconds // 60
                hours = minutes // 60
                if hours > 0:
                    daysago = f"{hours} hours ago"
                else:
                    daysago = f"{minutes} minutes ago"
            log.info("Using cached response from %s", daysago)
            return cached_data["data"]
        else:
            log.info("Cache is outdated.")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        log.warning("Failed to load cache: %s", e)
    return None

def cache_response(data: List[dict]):
    """Save the response to the cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("r") as f:
        json.dump({"date": datetime.now().isoformat(), "data": data}, f)
    log.info("Response cached successfully.")

# %% Models

class GenomeType(Enum):
    DNA = "DNA"
    RNA = "RNA"

class TypeEnum(Enum):
    BOTH = "both"
    PERTURBATION = "perturbation"
    SENSITIVITY = "sensitivity"

@dataclass
class MicroarrayType:
    label: str
    name: str

@dataclass
class Details:
    microarray_type: MicroarrayType

@dataclass
class AvailableDatatype:
    name: str
    genome_type: GenomeType
    source: Optional[str]
    details: Optional[Details]

    @classmethod
    def from_json(cls, data: dict) -> "AvailableDatatype":
        log.debug("Parsing AvailableDatatype from JSON: %s", data)
        return cls(
            data["name"],
            GenomeType(data["genomeType"]),
            data.get("source"),
            Details(
                MicroarrayType(
                    data["details"]["microarrayType"]["label"],
                    data["details"]["microarrayType"]["name"],
                )
            ) if data.get("details") else None,
        )

@dataclass
class Sensitivity:
    version: str
    source: str

@dataclass
class Publication:
    citation: str
    link: str

@dataclass
class VersionInfo:
    version: str
    dataset_type: Optional[TypeEnum]
    publication: List[Publication]

    @classmethod
    def from_json(cls, data: dict) -> "VersionInfo":
        log.debug("Parsing VersionInfo from JSON: %s", data)
        dataset_type = data.get("type", None)
        publist = [
            Publication(
                citation=pub["citation"],
                link=pub["link"],
            )
            for pub in data["publication"]
        ]
        return cls(
            data["version"],
            TypeEnum(dataset_type) if dataset_type else None,
            publist,
        )

@dataclass
class Dataset:
    name: str
    version_info: VersionInfo
    sensitivity: Sensitivity

    @classmethod
    def from_json(cls, data: dict) -> "Dataset":
        log.debug("Parsing Dataset from JSON: %s", data)
        return cls(
            data["name"],
            VersionInfo.from_json(data["versionInfo"]),
            Sensitivity(
                data["sensitivity"]["version"],
                data["sensitivity"]["source"],
            )
        )

@dataclass
class PharmacoSet:
    name: str
    doi: str
    download_link: str
    date_created: Optional[datetime]
    dataset: Dataset
    available_datatypes: List[AvailableDatatype] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> "PharmacoSet":
        log.debug("Parsing PharmacoSet from JSON: %s", data)
        date_created = data.get("dateCreated")
        if date_created:
            date_created = datetime.fromisoformat(date_created)
        return cls(
            data["name"],
            data["doi"],
            data["downloadLink"],
            date_created,
            Dataset.from_json(data["dataset"]),
            [
                AvailableDatatype.from_json(adt)
                for adt in data["availableDatatypes"]
            ]
        )

@dataclass
class PharmacoSetManager:
    psets: List[PharmacoSet] = field(default_factory=list)
    url: str = "https://orcestra.ca/api/psets/available"

    def __init__(self, force: bool = False) -> None:
        result = asyncio.run(self.fetch(force=force))
        if result and not isinstance(result, Exception):
            log.info(f"Successfully fetched {len(self.psets)} PharmacoSets.")

    async def fetch(self, force: bool = False) -> None:
        """Fetch and initialize PharmacoSets from the API."""
        with Progress(transient=True) as progress:
            task = progress.add_task("[cyan]Fetching PharmacoSets...", total=None)
            data = await self._fetch_psets(force=force)
            progress.update(task, completed=True)

        self.psets = [
            PharmacoSet.from_json(pset)
            for pset in data
        ]
        log.info("Loaded %d PharmacoSets.", len(self.psets))

    async def _fetch_psets(self, force: bool = False) -> List[dict]:
        """Fetch PharmacoSets from the API."""
        log.info("Fetching PharmacoSets (force=%s)...", force)
        if not force and (cached_data := get_cached_response()):
            return cached_data

        log.info("Making API call to %s", self.url)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                data = await response.json()
                log.info("Fetched %d PharmacoSets from API.", len(data))
                cache_response(data)
                return data

    @property
    def names(self) -> List[str]:
        return [pset.name for pset in self.psets]

    def __getitem__(self, name: str) -> PharmacoSet:
        try:
            return next(pset for pset in self.psets if pset.name == name)
        except StopIteration:
            closest_matches = self.find_similar(name)
            if closest_matches:
                suggestion_msg = f"PharmacoSet '{name}' not found"
                suggestion_msg += f"\nFound similar:\n\t{',\n\t'.join(closest_matches)}"
                raise ValueError(suggestion_msg)
            else:
                log.error("PharmacoSet '%s' not found and no similar names found.", name)
                raise ValueError(f"PharmacoSet '{name}' not found and no similar names found.")

    def find_similar(self, name: str, n: int = 3, cutoff: float = 0.3) -> List[str]:
        """Find similar PharmacoSet names."""
        log.debug("Finding similar names for: %s", name)
        return difflib.get_close_matches(name, self.names, n=n, cutoff=cutoff)

if __name__ == "__main__":
    import argparse
    from rich import print

    parser = argparse.ArgumentParser(description="Fetch PharmacoSets.")
    parser.add_argument("--force", action="store_true", help="Force fetch new PharmacoSets")
    args = parser.parse_args()

    log.info("Starting application...")
    psm = PharmacoSetManager(force=args.force)
    try:
        print(psm["GDSC"])
    except ValueError as e:
        log.error("Error: %s", e)
    print(psm["FIMM_2016"])
    log.info("Application finished.")