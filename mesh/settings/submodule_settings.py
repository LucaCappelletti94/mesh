"""Submodule defining the Submodule Settings interface."""

from abc import ABC, abstractmethod
from typing import List, Dict
from mesh.utils import DownloadObjective


class SubmoduleSettings(ABC):
    """Interface for Submodule Settings."""

    @abstractmethod
    def root_name(self) -> str:
        """Return the root name of the submodule."""

    @abstractmethod
    def included_codes(self) -> List[str]:
        """Return a list of submodule codes to include."""

    @abstractmethod
    def download_objectives(self) -> List[DownloadObjective]:
        """Return a list of download objectives for the submodule."""

    @abstractmethod
    def into_dict(self) -> Dict:
        """Return the submodule settings as a dictionary."""
