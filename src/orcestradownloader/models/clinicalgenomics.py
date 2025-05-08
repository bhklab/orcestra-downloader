"""
clinicalgenomics.py

This module provides the radiomicset class for managing radiogenomic datasets
in the OrcestraDownloader project.

Classes:
    clinicalgenomics: Class representing a clinicalgenomics dataset.
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class ClinicalGenomics(BaseModel):
    """
    Represents a radiogenomic dataset.

    Inherits from BaseModel for shared functionality.
    """

    @classmethod
    def from_json(cls, data: dict) -> ClinicalGenomics:
        """
        Create a ClinicalGenomics instance from a JSON object.

        Parameters
        ----------
        data : dict
            The JSON object containing data for the record.

        Returns
        -------
        ClinicalGenomics
            An instance of ClinicalGenomics.
        """
        log.debug("Parsing ClinicalGenomics from JSON: %s", data)
        return super().from_json(data)
