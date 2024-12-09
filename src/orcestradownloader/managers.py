from __future__ import annotations
import click
import difflib
import aiohttp
import asyncio
from rich.progress import Progress
from rich.logging import RichHandler
import logging
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import json
from .models.pset import PharmacoSet
from datetime import datetime
from rich.table import Table
from rich.console import Console

# Setup logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
log = logging.getLogger("orcestra")


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
    with CACHE_FILE.open("w") as f:
        json.dump({"date": datetime.now().isoformat(), "data": data}, f)
    log.info("Response cached successfully.")


@dataclass
class PharmacoSetManager:
    psets: List[PharmacoSet] = field(default_factory=list)
    url: str = "https://orcestra.ca/api/psets/available"

    def __init__(self, force: bool = False, psets: Optional[List[PharmacoSet]] = None) -> None:
        if psets is not None:
            self.psets = psets
        else:
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
            try: 
                all = [pset for pset in self.psets if pset.dataset.name == name] 
                if len(all) == 1:
                    return all[0]
                else:
                    log.warning(f"{len(all)} PharmacoSets found with name '{name}'. Returning first match.")
                    return all[0]

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

    def filter(self, **kwargs: Any) -> PharmacoSetManager: # type: ignore # noqa
        """Filter PharmacoSets based on attributes."""
        filtered_psets = [pset for pset in self.psets if all(getattr(pset, k) == v for k, v in kwargs.items())]
        if filtered_psets:
            return PharmacoSetManager(psets=filtered_psets)
        
        filtered_psets = [pset for pset in self.psets if any(getattr(pset.dataset, k) == v for k, v in kwargs.items())]
        if filtered_psets:
            return PharmacoSetManager(psets=filtered_psets)

        raise ValueError(f"No PharmacoSets found with attributes: {kwargs}")

    def print_table(self, sort: bool = True) -> None:
        """Print a table of PharmacoSets sorted by name."""
        if sort:
            sorted_psets = sorted(self.psets, key=lambda pset: pset.name.lower())
        else:
            sorted_psets = self.psets
        table = Table(title="PharmacoSets")

        table.add_column("PharmacoSet Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Dataset Name", justify="left", style="magenta")
        table.add_column("DOI", justify="left", style="yellow")
        table.add_column("Date Created", justify="left", style="green")
        table.add_column("Available Datatypes", justify="left", style="blue")

        for pset in sorted_psets:
            table.add_row(
                pset.name, 
                pset.dataset.name, 
                pset.doi, 
                pset.date_created.strftime("%Y-%m-%d") if pset.date_created else "N/A",
                ", ".join(pset.datatypes) if pset.datatypes else "N/A"
            )

        console = Console()
        console.print(table)

@click.command()
@click.option("--force", is_flag=True, help="Force fetch new PharmacoSets")
@click.argument(
	'names',
	nargs=-1,  # Allow multiple search inputs
	type=str,
	required=False,
)
def cli(names: List[str], force: bool = False, ) -> None:
    """Fetch PharmacoSets from the API."""
    log.info("Starting application...")
    if names:
        log.info("Searching for PharmacoSets with names: %s", names)

    psm = PharmacoSetManager(force=force)

    if not names:
        psm.print_table()
        return

    for name in names:
        filtered = psm.filter(name=name)
        filtered.psets = sorted(filtered.psets, key=lambda pset: pset.date_created or datetime.min, reverse=True)
        filtered.print_table(sort=False)

if __name__ == "__main__":
    cli()