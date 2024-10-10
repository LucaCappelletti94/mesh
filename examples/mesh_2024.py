"""Example building MESH 2024 dataset."""

from mesh.settings import DatasetSettings, ChemicalsAndDrugsSettings
from mesh import Dataset


def build_mesh_2024() -> Dataset:
    """Build MESH 2024 dataset."""
    cad: ChemicalsAndDrugsSettings = (
        ChemicalsAndDrugsSettings().include_all_submodules().include_smiles()
    )
    settings = DatasetSettings(version=2024).include_chemicals_and_drugs(cad)
    dataset = Dataset.build(settings)
    return dataset


if __name__ == "__main__":
    _ = build_mesh_2024()
