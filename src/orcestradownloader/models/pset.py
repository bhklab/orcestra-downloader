import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
log = logging.getLogger("orcestra")


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
