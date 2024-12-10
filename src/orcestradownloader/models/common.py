from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class GenomeType(Enum):
	DNA = 'DNA'
	RNA = 'RNA'


class TypeEnum(Enum):
	BOTH = 'both'
	PERTURBATION = 'perturbation'
	SENSITIVITY = 'sensitivity'


@dataclass
class Publication:
	citation: str
	link: str


@dataclass
class VersionInfo:
	version: str
	dataset_type: Optional[TypeEnum]
	publication: List[Publication]


@dataclass
class AvailableDatatype:
	name: str
	genome_type: Optional[GenomeType]
	source: Optional[str] = None


@dataclass
class Dataset:
	name: str
	version_info: VersionInfo


class AbstractRecord(ABC):
	"""Abstract base class for dataset records."""

	@classmethod
	@abstractmethod
	def from_json(cls, data: dict) -> 'AbstractRecord':
		pass

	@abstractmethod
	def print_summary(self) -> None:
		pass
