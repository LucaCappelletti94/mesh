# MESH

Python package helping to work with the [MESH dataset](https://www.ncbi.nlm.nih.gov/mesh/). This package is currently primarily focused on [the chemicals and drugs category of the MESH dataset](https://www.ncbi.nlm.nih.gov/mesh/1000068) and integrates the associated [PubChem database](https://pubchem.ncbi.nlm.nih.gov/) SMILES and InChI keys.

## Installation

At this moment, the package is not available on PyPI. To install it, you can clone the repository and install it using `pip`:

```bash
pip install .
```

## Usage

The package provides two main functionalities: downloading a pre-built MESH dataset and generating a custom MESH dataset. Once you have the dataset, you can use the `Dataset` class to work with it.

### Downloading a pre-built MESH dataset

While this package allows you to build a custom MESH dataset, since building the dataset requires reources, we also provide pre-built datasets which [we host on Zenodo](). The structure of any of the hosted tarballs is as follows:

```
mesh_chemistry_2024.tar.gz
├── chemicals.csv
├── descriptors.csv
├── chemicals_to_descriptors.csv
├── mesh_dag.csv
├── metadata.json
```

Where (you can see examples of these files just below):
- `chemicals.csv` contains information about chemicals and drugs.
- `descriptors.csv` contains information about descriptors.
- `chemicals_to_descriptors.csv` contains the relationships between chemicals and descriptors.
- `mesh_dag.csv` contains the Directed Acyclic Graph (DAG) of the MESH dataset.
- `metadata.json` contains metadata about the dataset.

To download a pre-built dataset, you can use the following code:

```python
from mesh import Dataset

dataset = Dataset.load("mesh_chemistry_2024")
```

Find the available rasterized datasets [on Zenodo]().

Here's some statistics regarding the rasterized MESH datasets, all created with the same settings described in the next section:

| Version name | Number of nodes | Number of edges | Number of chemicals  | Number of descriptors |
|--------------|-----------------|-----------------|----------------------|-----------------------|
| MESH 2024    | 334220          | 367694          | 323679               | 10542                 |
| MESH 2023    | 332999          | 365801          | 322591               | 10409                 |
| MESH 2022    | 330106          | 364653          | 319739               | 10367                 |
| MESH 2021    | 328884          | 363505          | 318391               | 10325                 |

### Generating a custom MESH dataset

The package provides a `Dataset` class that allows you to work with the MESH dataset. The dataset is built using the `DatasetSettings` class, which allows you to specify which parts of the dataset you want to include. The `ChemicalsAndDrugsSettings` class allows you to specify which parts of the chemicals and drugs category you want to include.

Particularly helpful, is the ability to include SMILES and InChI keys for the chemicals and drugs. This is done by specifying the `include_smiles` and `include_inchi_keys` methods of the `ChemicalsAndDrugsSettings` class.

```python
from mesh.settings import DatasetSettings, ChemicalsAndDrugsSettings
from mesh import Dataset


def build_mesh_chemistry_2024() -> Dataset:
    """Build MESH 2024 dataset."""
    # First, we need to define the settings for the dataset.
    cad: ChemicalsAndDrugsSettings = (
        ChemicalsAndDrugsSettings()
        # In this case, we are including all of the submodules of
        # categories of chemicals and drugs.
        .include_all_submodules()
        # We also want to include SMILES, which we obtain from the
        # PUBCHEM database.
        .include_smiles()
        # Analogously, we want to include InChI keys, which we obtain
        # from the PUBCHEM database.
        .include_inchi_keys()
    )
    settings = (
        # We are using the MESH 2024 version.
        DatasetSettings(version=2024)
        # We want to retrieve data only regarding chemicals and drugs.
        .include_chemicals_and_drugs(cad)
        # And we want to print the progress of the dataset retrieval.
        .set_verbose(True)
    )
    # Now, we build the dataset. This will download the necessary files
    # and rasterize the dataset.
    dataset = Dataset.build(settings)
    return dataset


if __name__ == "__main__":
    # We build the MESH 2024 dataset.
    mesh_chemistry_2024: Dataset = build_mesh_chemistry_2024()
    # And we save it to disk.
    mesh_chemistry_2024.save("mesh_chemistry_2024", tarball=False)
```

#### Resulting CSVs

The resulting CSVs will be saved in the `mesh_chemistry_2024` directory. The directory will contain the following CSVs:

##### `chemicals.csv`

|unique_identifier|name                                   |compound_id|substance_id|smiles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |inchi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |inchikey                   |
|-----------------|---------------------------------------|-----------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
|C000002          |bevonium                               |31800.0    |500762995.0 |C[N+]1(CCCCC1COC(=O)C(C2=CC=CC=C2)(C3=CC=CC=C3)O)C                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |InChI=1S/C22H28NO3/c1-23(2)16-10-9-15-20(23)17-26-21(24)22(25,18-11-5-3-6-12-18)19-13-7-4-8-14-19/h3-8,11-14,20,25H,9-10,15-17H2,1-2H3/q+1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |UHUMRJKDOOEQIG-UHFFFAOYSA-N|
|C000009          |N-acetylglucosaminylasparagine         |123826.0   |500203198.0 |CC(=O)N[C@@H]1[C@H]([C@@H]([C@H](O[C@H]1NC(=O)C[C@@H](C(=O)O)N)CO)O)O                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |InChI=1S/C12H21N3O8/c1-4(17)14-8-10(20)9(19)6(3-16)23-11(8)15-7(18)2-5(13)12(21)22/h5-6,8-11,16,19-20H,2-3,13H2,1H3,(H,14,17)(H,15,18)(H,21,22)/t5-,6+,8+,9+,10+,11+/m0/s1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |YTTRPBWEMMPYSW-HRRFRDKFSA-N|
|C000011          |5-(n-acetaminophenylazo)-8-oxyquinoline|114081.0   |484035752.0 |CC(=O)NC1=CC=C(C=C1)N=NC2=C3C=CC=NC3=C(C=C2)O                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |InChI=1S/C17H14N4O2/c1-11(22)19-12-4-6-13(7-5-12)20-21-15-8-9-16(23)17-14(15)3-2-10-18-17/h2-10,23H,1H3,(H,19,22)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |DKRPSSOODLBKPQ-UHFFFAOYSA-N|
|C000015          |N-acetyl-L-arginine                    |67427.0    |500710457.0 |CC(=O)N[C@@H](CCCN=C(N)N)C(=O)O                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |InChI=1S/C8H16N4O3/c1-5(13)12-6(7(14)15)3-2-4-11-8(9)10/h6H,2-4H2,1H3,(H,12,13)(H,14,15)(H4,9,10,11)/t6-/m0/s1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |SNEIUMQYRCDYCH-LURJTMIESA-N|
|C000020          |N-acetylneuraminoyllactose             |           |489852514.0 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                           |
|C000021          |acetylnovadral                         |           |            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                           |


##### `descriptors.csv`

| unique_identifier | name                              | compound_id    | substance_id   | smiles                                                                                                        | inchikey                         |
|-------------------|-----------------------------------|----------------|----------------|---------------------------------------------------------------------------------------------------------------|----------------------------------|
| D000001           | Calcimycin                        | 139593372.0    | 500766157.0    | C[C@@H]1CCC2([C@H](C[C@@H]([C@@H](O2)C(C)C(=O)C3=CC=CN3)C)C)O[C@@H]1CC4=NC5=C(O4)C=CC(=C5C(=O)O)NC             | HIYAVKIYRIFSCZ-LGHBZWQHSA-N      |
| D000002           | Temefos                           | 5392.0         | 500974612.0    | COP(=S)(OC)OC1=CC=C(C=C1)SC2=CC=C(C=C2)OP(=S)(OC)OC                                                            | WWJZWCUNLNYYAU-UHFFFAOYSA-N      |
| D000017           | ABO Blood-Group System            |                |                |                                                                                                               |                                  |
| D000019           | Abortifacient Agents              |                |                |                                                                                                               |                                  |
| D000020           | Abortifacient Agents, Nonsteroidal |                |                |                                                                                                               |                                  |
| D000021           | Abortifacient Agents, Steroidal   |                |                |                                                                                                               |                                  |
| D000036           | Abrin                             |                | 486451862.0    |                                                                                                               |                                  |
| D000040           | Abscisic Acid                     | 5702609.0      | 500195639.0    | CC1=CC(=O)CC([C@]1(/C=C/C(=C/C(=O)O)/C)O)(C)C                                                                  | JLIDBLDQVAYHNE-IBPUIESWSA-N      |



##### `chemicals_to_descriptors.csv`

| chemical | descriptor |
|----------|------------|
| C000002  | D001561    |
| C000006  | D061389    |
| C000009  | D000117    |
| C000011  | D015125    |
| C000015  | D001120    |
| C000020  | D007785    |


##### `mesh_dag.csv`

| parent  | child      |
|---------|------------|
| D000001 | D000095662 |
| D000001 | D001583    |
| D000002 | D063086    |
| D000017 | D001789    |
| D000019 | D012102    |
| D000020 | D000019    |
| D000021 | D000019    |

##### `metadata.json`

```json
{
    "version": {
        "version": 2024,
        "descriptors": "https://nlmpubs.nlm.nih.gov/projects/mesh/2024/asciimesh/20240101/d2024.bin",
        "chemicals": "https://nlmpubs.nlm.nih.gov/projects/mesh/2024/asciimesh/20240101/c2024.bin"
    },
    "roots": [
        {
            "root": "Chemicals and Drugs",
            "included_codes": [
                "D01",
                "D02",
                "D03",
                "D04",
                "D05",
                "D06",
                "D08",
                "D09",
                "D10",
                "D12",
                "D13",
                "D20",
                "D23",
                "D25",
                "D26",
                "D27"
            ],
            "include_smiles": true
        }
    ],
    "downloads_directory": "downloads"
}
```

### To NetworkX

Since the MESH dataset is a Directed Acyclic Graph (DAG), you can convert it to a NetworkX graph. This is done by calling the `to_networkx` method of the `Dataset` class.

```python
import networkx as nx

# We convert the MESH dataset to a NetworkX graph.
graph: nx.DiGraph = mesh_chemistry_2024.to_networkx()

# Now, we can use the NetworkX graph as we would any other NetworkX graph.
print(nx.info(graph))
```

In this case, the output will be:

```
DiGraph with 334220 nodes and 367694 edges 
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.