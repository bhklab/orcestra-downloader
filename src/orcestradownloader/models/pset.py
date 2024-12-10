from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from rich.table import Table
from rich.console import Console
from orcestradownloader.models.common import (
    Dataset, AvailableDatatype, AbstractRecord, VersionInfo, Publication, GenomeType, TypeEnum
)
from orcestradownloader.logging_config import logger as log

@dataclass
class PharmacoSet(AbstractRecord):
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
        dataset_type = data.get("dataset", {}).get("versionInfo", {}).get("type")
        version_info = VersionInfo(
            version=data["dataset"]["versionInfo"]["version"],
            dataset_type=TypeEnum(dataset_type) if dataset_type else None,
            publication=[
                Publication(**pub) for pub in data["dataset"]["versionInfo"]["publication"]
            ]
        )
        dataset = Dataset(
            name=data["dataset"]["name"],
            version_info=version_info
        )
        datatypes = [
            AvailableDatatype(
                name=adt["name"],
                genome_type=GenomeType(adt["genomeType"]),
                source=adt.get("source")
            )
            for adt in data.get("availableDatatypes", [])
        ]
        return cls(
            name=data["name"],
            doi=data["doi"],
            download_link=data["downloadLink"],
            date_created=date_created,
            dataset=dataset,
            available_datatypes=datatypes
        )

    @property
    def datatypes(self) -> List[str]:
            return [adt.name for adt in self.available_datatypes]

    def print_summary(self) -> None:
        """Print a summary table for the PharmacoSet."""
        table = Table(title="PharmacoSet Summary")

        table.add_column("Field", style="bold cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Name", self.name)
        table.add_row("Dataset Name", self.dataset.name)
        table.add_row("DOI", self.doi)
        table.add_row("Date Created", self.date_created.isoformat() if self.date_created else "N/A")
        table.add_row("Download Link", self.download_link)
        table.add_row("Dataset Sensitivity Version", self.dataset.version_info.version)
        table.add_row("Available Datatypes", ", ".join([dt.name for dt in self.available_datatypes]))

        console = Console()
        console.print(table)

if __name__ == "__main__":
    from pathlib import Path
    import json
    from rich import print
    cache_file = Path.home() / ".cache/orcestradownloader/psets.json"
    with cache_file.open("r") as f:
        data = json.load(f)

    psets = [
        PharmacoSet.from_json(pset)
        for pset in data["data"]
    ]
    print(psets)
