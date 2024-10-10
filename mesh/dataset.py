"""Submodule providing the Dataset class, representing an instance of the MESH dataset."""

from typing import List, Dict
import os
from downloaders import BaseDownloader
from tqdm.auto import tqdm
from mesh.settings import DatasetSettings
from mesh.descriptors_reader import MESHDescriptorsReader, MESHDescriptor
from mesh.chemicals_reader import MESHChemicalsReader, MESHChemical
from mesh.qualifiers_reader import MESHQualifiersReader, MESHQualifier


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
            verbose=settings.verbose,
        )
        paths: List[str] = []
        urls: List[str] = []

        for download_objective in settings.download_objectives():
            paths.append(
                os.path.join(
                    settings.downloads_directory,
                    download_objective.path,
                )
            )
            urls.append(download_objective.url)

        downloader.download(urls=urls, paths=paths)

        descriptors: List[MESHDescriptor] = list(
            MESHDescriptorsReader(settings=settings)
        )

        chemicals: List[MESHChemical] = list(MESHChemicalsReader(settings=settings))
        qualifiers: List[MESHQualifier] = list(MESHQualifiersReader(settings=settings))

        enrichment_procedures = settings.enrichment_procedures()

        for enricher in tqdm(
            enrichment_procedures,
            desc="Enriching dataset",
            disable=not settings.verbose,
            leave=False,
            dynamic_ncols=True,
        ):
            for descriptor in descriptors:
                enricher.enrich(entry=descriptor)
            for chemical in chemicals:
                enricher.enrich(entry=chemical)
            for qualifier in qualifiers:
                enricher.enrich(entry=qualifier)

        print(descriptors[:5])
        print(chemicals[:5])
        print(qualifiers[:5])

        return Dataset(metadata=settings.into_dict())
