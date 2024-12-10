from dataclasses import dataclass
from typing import List, Optional
from .common import AbstractRecord, Dataset, AvailableDatatype, Publication, VersionInfo, GenomeType
from datetime import datetime
@dataclass
class DatasetRecord(AbstractRecord):
		name: str
		doi: str
		download_link: str
		date_created: Optional[datetime]
		dataset: Dataset
		available_datatypes: List[AvailableDatatype]

		@classmethod
		def from_json(cls, record: dict) -> "DatasetRecord":
				publications = [
						Publication(**pub) for pub in record["dataset"]["versionInfo"]["publication"]
				]
				version_info = VersionInfo(
						version=record["dataset"]["versionInfo"]["version"],
						dataset_type=record["dataset"]["versionInfo"].get("type"),
						publication=publications
				)
				dataset = Dataset(
						name=record["dataset"]["name"],
						version_info=version_info
				)

				datatypes = [
						AvailableDatatype(
								name=adt["name"],
								genome_type=GenomeType(adt["genomeType"]),
								source=adt.get("source")
						)
						for adt in record.get("availableDatatypes", [])
				]

				date_created = record.get("dateCreated")
				if date_created:
						date_created = datetime.fromisoformat(date_created)
				return cls(
						name=record["name"],
						doi=record["doi"],
						download_link=record["downloadLink"],
						date_created=date_created,
						dataset=dataset,
						available_datatypes=datatypes
				)

		@property
		def datatypes(self) -> List[str]:
				return [adt.name for adt in self.available_datatypes]

		def print_summary(self) -> None:
				"""Print a summary for the DatasetRecord."""
				print(f"Dataset Record: {self.name}")
				print(f"DOI: {self.doi}")
				print(f"Download Link: {self.download_link}")
				print(f"Date Created: {self.date_created}")
				print(f"Dataset Name: {self.dataset.name}")
				print(f"Available Datatypes: {', '.join([adt.name for adt in self.available_datatypes])}")