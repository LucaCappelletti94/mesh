"""Settings regarding the Chemicals and Drugs section of the MESH DAG."""

from typing import List, Dict
import compress_json
from mesh.settings.submodule_settings import SubmoduleSettings
from mesh.utils import DownloadObjective


class ChemicalsAndDrugsSettings(SubmoduleSettings):
    """Class defining the settings for the Chemicals and Drugs section of the MESH dataset."""

    def __init__(self):
        """Initialize the ChemicalsAndDrugsSettings class."""
        self._included_codes: List[str] = []
        self._codes: List[Dict[str, str]] = compress_json.local_load(
            "chemicals_and_drugs_codes.json"
        )
        self._include_smiles: bool = False

    def root_name(self) -> str:
        """Return the root of the Chemicals and Drugs section."""
        return "Chemicals and Drugs"

    def included_codes(self) -> List[str]:
        """Return a list of submodule names to include."""
        return self._included_codes

    def into_dict(self) -> Dict:
        """Return the submodule settings as a dictionary."""
        return {
            "root": self.root_name(),
            "included_codes": self._included_codes,
            "include_smiles": self._include_smiles,
        }

    def download_objectives(self) -> List[DownloadObjective]:
        """Return a list of download objectives for the submodule."""
        download_objectives: List[DownloadObjective] = []
        pubchem_metadata = compress_json.local_load("pubchem.json")
        if self._include_smiles:
            download_objectives.extend(
                [
                    DownloadObjective(
                        url=pubchem_metadata["CID-MeSH"]["url"],
                        path=pubchem_metadata["CID-MeSH"]["file_name"],
                    ),
                    DownloadObjective(
                        url=pubchem_metadata["CID-SMILES"]["url"],
                        path=pubchem_metadata["CID-SMILES"]["file_name"],
                    ),
                ]
            )
        return download_objectives

    def _include_code(self, name: str):
        """Include a code in the dataset."""
        for code in self._codes:
            if code["name"] == name:
                self._included_codes.append(code["code"])
                return
        raise ValueError(f"Code {name} not found.")

    def include_inorganic_chemicals(self) -> "ChemicalsAndDrugsSettings":
        """Include inorganic chemicals in the dataset."""
        self._include_code("Inorganic Chemicals")
        return self

    def include_organic_chemicals(self) -> "ChemicalsAndDrugsSettings":
        """Include organic chemicals in the dataset."""
        self._include_code("Organic Chemicals")
        return self

    def include_heterocyclic_compounds(self) -> "ChemicalsAndDrugsSettings":
        """Include heterocyclic compounds in the dataset."""
        self._include_code("Heterocyclic Compounds")
        return self

    def include_polycyclic_compounds(self) -> "ChemicalsAndDrugsSettings":
        """Include polycyclic compounds in the dataset."""
        self._include_code("Polycyclic Compounds")
        return self

    def include_macromolecular_substances(self) -> "ChemicalsAndDrugsSettings":
        """Include macromolecular substances in the dataset."""
        self._include_code("Macromolecular Substances")
        return self

    def include_hormones_hormone_substitutes_hormone_antagonists(
        self,
    ) -> "ChemicalsAndDrugsSettings":
        """Include hormones, hormone substitutes, and hormone antagonists in the dataset."""
        self._include_code("Hormones, Hormone Substitutes, and Hormone Antagonists")
        return self

    def include_enzymes_and_coenzymes(self) -> "ChemicalsAndDrugsSettings":
        """Include enzymes and coenzymes in the dataset."""
        self._include_code("Enzymes and Coenzymes")
        return self

    def include_carbohydrates(self) -> "ChemicalsAndDrugsSettings":
        """Include carbohydrates in the dataset."""
        self._include_code("Carbohydrates")
        return self

    def include_lipids(self) -> "ChemicalsAndDrugsSettings":
        """Include lipids in the dataset."""
        self._include_code("Lipids")
        return self

    def include_amino_acids_peptides_and_proteins(self) -> "ChemicalsAndDrugsSettings":
        """Include amino acids, peptides, and proteins in the dataset."""
        self._include_code("Amino Acids, Peptides, and Proteins")
        return self

    def include_nucleic_acids_nucleotides_and_nucleosides(
        self,
    ) -> "ChemicalsAndDrugsSettings":
        """Include nucleic acids, nucleotides, and nucleosides in the dataset."""
        self._include_code("Nucleic Acids, Nucleotides, and Nucleosides")
        return self

    def include_complex_mixtures(self) -> "ChemicalsAndDrugsSettings":
        """Include complex mixtures in the dataset."""
        self._include_code("Complex Mixtures")
        return self

    def include_biological_factors(self) -> "ChemicalsAndDrugsSettings":
        """Include biological factors in the dataset."""
        self._include_code("Biological Factors")
        return self

    def include_biomedical_and_dental_materials(self) -> "ChemicalsAndDrugsSettings":
        """Include biomedical and dental materials in the dataset."""
        self._include_code("Biomedical and Dental Materials")
        return self

    def include_pharmaceutical_preparations(self) -> "ChemicalsAndDrugsSettings":
        """Include pharmaceutical preparations in the dataset."""
        self._include_code("Pharmaceutical Preparations")
        return self

    def include_chemical_actions_and_uses(self) -> "ChemicalsAndDrugsSettings":
        """Include chemical actions and uses in the dataset."""
        self._include_code("Chemical Actions and Uses")
        return self

    def include_all_submodules(self) -> "ChemicalsAndDrugsSettings":
        """Include all codes in the dataset."""
        for code in self._codes:
            self._included_codes.append(code["code"])
        return self

    def include_smiles(self) -> "ChemicalsAndDrugsSettings":
        """Return whether to include SMILES in the dataset."""
        self._include_smiles = True
        return self
