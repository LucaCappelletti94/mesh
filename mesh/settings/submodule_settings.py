"""Submodule defining the Submodule Settings interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Type
from mesh.enrichers import Enricher


class SubmoduleSettings(ABC):
    """Interface for Submodule Settings."""

    @abstractmethod
    def root_name(self) -> str:
        """Return the root name of the submodule."""

    @abstractmethod
    def allowed_mesh_dag_numbers(self) -> List[str]:
        """Return a list of allowed MeSH tree numbers."""

    @abstractmethod
    def into_dict(self) -> Dict:
        """Return the submodule settings as a dictionary."""

    @abstractmethod
    def enrichment_procedures(
        self, downloads_directory: str, verbose: bool
    ) -> List[Type[Enricher]]:
        """Return a list of enrichment procedures for the dataset."""
