"""Submodule defining the settings for the MESH dataset to rasterize."""

from typing import List, Type, Dict
import os
import compress_json
from mesh.settings.chemicals_and_drugs_settings import ChemicalsAndDrugsSettings
from mesh.settings.submodule_settings import SubmoduleSettings
from mesh.utils import DownloadObjective
from mesh.enrichers import Enricher


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
        self._downloads_directory: str = "downloads"
        self._verbose: bool = False

    def enrichment_procedures(self) -> List[Enricher]:
        """Return a list of enrichment procedures for the dataset."""
        enrichers: List[Enricher] = []
        for root in self._roots:
            enrichers.extend(root.enrichment_procedures(
                downloads_directory=self._downloads_directory,
                verbose=self._verbose,
            ))
        return enrichers

    @property
    def verbose(self) -> bool:
        """Return the verbosity of the dataset."""
        return self._verbose

    @property
    def allowed_root_letters(self) -> List[str]:
        """Return a list of allowed root letters."""
        root_letters: List[str] = []
        root_letters_metadata: List[Dict[str, str]] = compress_json.local_load(
            "root_letters.json"
        )
        for root in self._roots:
            for entry in root_letters_metadata:
                if root.root_name() == entry["name"]:
                    root_letters.append(entry["letter"])
        return root_letters

    @property
    def allowed_mesh_tree_numbers(self) -> List[str]:
        """Return a list of allowed MeSH tree numbers."""
        mesh_tree_numbers: List[str] = []
        for root in self._roots:
            mesh_tree_numbers.extend(root.allowed_mesh_tree_numbers())
        return mesh_tree_numbers

    def set_verbose(self, verbose: bool) -> "DatasetSettings":
        """Set the verbosity of the dataset."""
        assert isinstance(verbose, bool)
        self._verbose = verbose
        return self

    def into_dict(self) -> Dict:
        """Return the dataset settings as a dictionary."""
        return {
            "version": self._version,
            "roots": [root.into_dict() for root in self._roots],
            "downloads_directory": self._downloads_directory,
        }

    @property
    def downloads_directory(self) -> str:
        """Return the download directory for the dataset."""
        return self._downloads_directory

    @property
    def version(self) -> int:
        """Return the version of the dataset."""
        return self._version["version"]

    @property
    def descriptors_directory(self) -> str:
        """Return the directory of the descriptors."""
        return os.path.join(
            str(self._version["version"]),
            "descriptors.txt",
        )

    @property
    def chemicals_directory(self) -> str:
        """Return the directory of the chemicals."""
        return os.path.join(
            str(self._version["version"]),
            "chemicals.txt",
        )

    @property
    def qualifiers_directory(self) -> str:
        """Return the directory of the qualifiers."""
        return os.path.join(
            str(self._version["version"]),
            "qualifiers.txt",
        )

    def download_objectives(self) -> List[DownloadObjective]:
        """Return a list of download objectives for the dataset."""
        return [
            DownloadObjective(
                url=self._version["descriptors"],
                path=self.descriptors_directory,
            ),
            DownloadObjective(
                url=self._version["chemicals"],
                path=self.chemicals_directory,
            ),
            DownloadObjective(
                url=self._version["qualifiers"],
                path=self.qualifiers_directory,
            ),
        ]

    def include_chemicals_and_drugs(
        self, settings: ChemicalsAndDrugsSettings
    ) -> "DatasetSettings":
        """Include diseases in the dataset."""
        assert isinstance(settings, ChemicalsAndDrugsSettings)
        self._roots.append(settings)
        return self

    def set_downloads_directory(self, directory: str) -> "DatasetSettings":
        """Set the download directory for the dataset."""
        assert isinstance(directory, str)
        assert len(directory) > 0
        self._downloads_directory = directory
        return self
