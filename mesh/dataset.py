"""Submodule providing the Dataset class, representing an instance of the MESH dataset."""

from typing import List, Dict
import os
from downloaders import BaseDownloader
from mesh.settings import DatasetSettings


class Dataset:
    """Class representing a MESH dataset."""

    def __init__(self, metadata: Dict):
        """Initialize the Dataset class."""

    @staticmethod
    def build(settings: DatasetSettings) -> "Dataset":
        """Rasterize the dataset."""
        assert isinstance(settings, DatasetSettings)
        downloader = BaseDownloader(
            process_number=1,
        )
        paths: List[str] = []
        urls: List[str] = []

        for download_objective in settings.download_objectives():
            paths.append(
                os.path.join(
                    settings.download_directory,
                    download_objective.path,
                )
            )
            urls.append(download_objective.url)

        downloader.download(urls=urls, paths=paths)

        return Dataset(metadata=settings.into_dict())
