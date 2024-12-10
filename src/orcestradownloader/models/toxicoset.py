from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from orcestradownloader.models.common import AvailableDatatype, Dataset, VersionInfo, Publication, GenomeType
from orcestradownloader.logging_config import logger as log

@dataclass
class ToxicoSet:
    name: str
    doi: str
    download_link: str
    date_created: Optional[datetime]
    dataset: Dataset
    available_datatypes: List[AvailableDatatype] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: dict) -> "ToxicoSet":
        log.debug("Parsing ToxicoSet from JSON: %s", data)

        # Parse the dataset information
        dataset_data = data["dataset"]
        version_info = VersionInfo(
            version=dataset_data["versionInfo"]["version"],
            dataset_type=None,  # "type" is null in the provided data
            publication=[
                Publication(**pub) for pub in dataset_data["versionInfo"]["publication"]
            ]
        )
        dataset = Dataset(
            name=dataset_data["name"],
            version_info=version_info,
        )

        # Parse available datatypes
        datatypes = [
            AvailableDatatype(
                name=datatype.get("name"),
                genome_type=GenomeType(datatype["genomeType"]) if "genomeType" in datatype else None,
                source=datatype.get("source"),
            )
            for datatype in data.get("availableDatatypes", [])
        ]

        # Parse the ToxicoSet instance
        date_created = data.get("dateCreated")
        if date_created:
            date_created = datetime.fromisoformat(date_created.rstrip("Z"))  # Remove "Z" for proper parsing

        return cls(
            name=data["name"],
            doi=data["doi"],
            download_link=data["downloadLink"],
            date_created=date_created,
            dataset=dataset,
            available_datatypes=datatypes,
        )

    @property
    def datatypes(self) -> List[str]:
        return [datatype.name for datatype in self.available_datatypes]

    def print_summary(self) -> None:
        """Print a summary of the ToxicoSet."""
        from rich.console import Console
        from rich.table import Table

        table = Table(title="ToxicoSet Summary")

        table.add_column("Field", style="bold cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Name", self.name)
        table.add_row("DOI", self.doi)
        table.add_row("Date Created", self.date_created.isoformat() if self.date_created else "N/A")
        table.add_row("Download Link", self.download_link)
        table.add_row("Dataset Name", self.dataset.name)
        table.add_row("Dataset Version", self.dataset.version_info.version)
        table.add_row("Sensitivity Source", self.dataset.version_info.publication[0].link if self.dataset.version_info.publication else "N/A")
        table.add_row("Available Datatypes", ", ".join(self.datatypes) if self.datatypes else "N/A")

        console = Console()
        console.print(table)

if __name__ == "__main__":
    from pathlib import Path
    import json
    from rich import print
    cache_file = Path.home() / ".cache/orcestradownloader/toxicoset.json"
    with cache_file.open("r") as f:
        data = json.load(f)

    radiosets = [
        ToxicoSet.from_json(radioset)
        for radioset in data["data"]
    ]
    print(radiosets)