"""Submodule defining the settings for the MESH dataset to rasterize."""

from typing import List, Type, Dict
import os
import compress_json
from mesh.settings.chemicals_and_drugs_settings import ChemicalsAndDrugsSettings
from mesh.settings.submodule_settings import SubmoduleSettings
from mesh.utils import DownloadObjective


class DatasetSettings:
    """Class defining the settings for the MESH dataset to rasterize."""

    def __init__(self, version: int = 2024):
        """Initialize the DatasetSettings class."""
        assert isinstance(version, int)
        self._version: Dict[str, str] = None
        for version_metadata in compress_json.local_load("versions.json"):
            if version_metadata["version"] == version:
                self._version = version_metadata
                break
        if self._version is None:
            raise ValueError(f"Version {version} not found.")

        self._roots: List[Type[SubmoduleSettings]] = []
        self._download_directory: str = "downloads"

    def into_dict(self) -> Dict:
        """Return the dataset settings as a dictionary."""
        return {
            "version": self._version,
            "roots": [root.into_dict() for root in self._roots],
            "download_directory": self._download_directory,
        }

    @property
    def download_directory(self) -> str:
        """Return the download directory for the dataset."""
        return self._download_directory

    def download_objectives(self) -> List[DownloadObjective]:
        """Return a list of download objectives for the dataset."""
        download_objectives: List[DownloadObjective] = [
            DownloadObjective(
                url=self._version["descriptors"],
                path=os.path.join(
                    str(self._version["version"]),
                    "descriptors.txt",
                ),
            ),
            DownloadObjective(
                url=self._version["chemicals"],
                path=os.path.join(
                    str(self._version["version"]),
                    "chemicals.txt",
                ),
            ),
        ]

        for root in self._roots:
            download_objectives.extend(root.download_objectives())
        return download_objectives

    def include_chemicals_and_drugs(
        self, settings: ChemicalsAndDrugsSettings
    ) -> "DatasetSettings":
        """Include diseases in the dataset."""
        assert isinstance(settings, ChemicalsAndDrugsSettings)
        self._roots.append(settings)
        return self

    def set_download_directory(self, directory: str) -> "DatasetSettings":
        """Set the download directory for the dataset."""
        assert isinstance(directory, str)
        assert len(directory) > 0
        self._download_directory = directory
        return self
