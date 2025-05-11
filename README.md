# BioThings Typed Client

[![Tests](https://github.com/longevity-genie/biothings-typed-client/actions/workflows/tests.yml/badge.svg)](https://github.com/longevity-genie/biothings-typed-client/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/biothings-typed-client.svg)](https://badge.fury.io/py/biothings-typed-client)

## About BioThings.io

[BioThings.io](https://biothings.io/) is a platform that provides a network of high-performance biomedical APIs and tools for building FAIR (Findable, Accessible, Interoperable, and Reusable) data services. The platform includes several key components:

- **Core BioThings APIs**:
  - [MyGene.info](https://mygene.info/) - Gene Annotation Service
  - [MyVariant.info](https://myvariant.info/) - Variant Annotation Service
  - [MyChem.info](https://mychem.info/) - Chemical and Drug Annotation Service
  - [MyDisease.info](http://mydisease.info/) - Disease Annotation Service
  - Taxonomy API - For querying taxonomic information

This typed client library is built on top of the BioThings ecosystem, providing type-safe access to these services through Python.

## Project Description

A strongly-typed Python wrapper around the [BioThings Client](https://github.com/biothings/biothings_client.py) library, providing type safety and better IDE support through Python's type hints and Pydantic models.

## Features

- **Type Safety & Validation**: Leverages Pydantic models for runtime data validation and type checking.
- **Enhanced IDE Support**: Full autocompletion and static analysis in modern IDEs
- **Synchronous & Asynchronous**: Support for both sync and async operations
- **Helper Methods**: Additional utility methods for common operations
- **Compatibility**: Maintains full compatibility with the original BioThings client

## Installation

### Clone the Repository

```bash
git clone https://github.com/longevity-genie/biothings-typed-client.git
cd biothings-typed-client
```

### Using pip

```bash
pip install biothings-typed-client
```

#### Setting Up for Development

If you want to contribute to this repository:

1.  Clone the repository (if you haven't already):
    ```bash
    git clone https://github.com/longevity-genie/biothings-typed-client.git
    cd biothings-typed-client
    ```

2.  Install UV:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  Create and activate a virtual environment:
    ```bash
    uv venv
    source .venv/bin/activate  # On Unix/macOS
    # or
    .venv\Scripts\activate  # On Windows
    ```

4.  Install all dependencies, including development tools:
    ```bash
    uv sync
    ```
    This command reads the `pyproject.toml` file and installs the package in editable mode along with all its dependencies and optional dependencies (like those needed for testing and development).

## Quick Start

### Synchronous Client

```python
from biothings_typed_client.variants import VariantClient

# Initialize the client
client = VariantClient()

# Get a single variant
variant = client.getvariant("chr7:g.140453134T>C")
if variant:
    print(f"Variant ID: {variant.get_variant_id()}")
    print(f"Chromosome: {variant.chrom}")
    print(f"Position: {variant.vcf.position}")
    print(f"Reference: {variant.vcf.ref}")
    print(f"Alternative: {variant.vcf.alt}")

# Get multiple variants
variants = client.getvariants(["chr7:g.140453134T>C", "chr9:g.107620835G>A"])
for variant in variants:
    print(f"Found variant: {variant.get_variant_id()}")

# Query variants
results = client.query("dbnsfp.genename:cdk2", size=5)
for hit in results["hits"]:
    print(f"Found variant: {hit['_id']}")
```

### Asynchronous Client

```python
import asyncio
from biothings_typed_client.variants import VariantClientAsync

async def main():
    # Initialize the client
    client = VariantClientAsync()
    
    # Get a single variant
    variant = await client.getvariant("chr7:g.140453134T>C")
    if variant:
        print(f"Variant ID: {variant.get_variant_id()}")
        print(f"Has clinical significance: {variant.has_clinical_significance()}")
        print(f"Has functional predictions: {variant.has_functional_predictions()}")
    
    # Query variants
    results = await client.query("dbnsfp.genename:cdk2", size=5)
    print("\nQuery results:")
    print(results)

# Run the async code
asyncio.run(main())
```

### Gene Client Examples

#### Synchronous Gene Client

```python
from biothings_typed_client.genes import GeneClient

# Initialize the client
client = GeneClient()

# Get a single gene
gene = client.getgene("1017")  # Using Entrez ID
if gene:
    print(f"Gene ID: {gene.id}")
    print(f"Symbol: {gene.symbol}")
    print(f"Name: {gene.name}")

# Get multiple genes
genes = client.getgenes(["1017", "1018"])  # Using Entrez IDs
for gene in genes:
    print(f"Found gene: {gene.symbol} ({gene.name})")

# Query genes
results = client.query("symbol:CDK2", size=5)
for hit in results["hits"]:
    print(f"Found gene: {hit['symbol']} ({hit['name']})")

# Batch query genes
genes = client.querymany(["CDK2", "BRCA1"], scopes=["symbol"], size=1)
for gene in genes:
    print(f"Found gene: {gene['symbol']} ({gene['name']})")
```

#### Asynchronous Gene Client

```python
import asyncio
from biothings_typed_client.genes import GeneClientAsync

async def main():
    # Initialize the client
    client = GeneClientAsync()
    
    # Get a single gene
    gene = await client.getgene("1017")  # Using Entrez ID
    if gene:
        print(f"Gene ID: {gene.id}")
        print(f"Symbol: {gene.symbol}")
        print(f"Name: {gene.name}")
    
    # Query genes
    results = await client.query("symbol:CDK2", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found gene: {hit['symbol']} ({hit['name']})")

# Run the async code
asyncio.run(main())
```

### Chemical Client Examples

#### Synchronous Chemical Client

```python
from biothings_typed_client.chem import ChemClient

# Initialize the client
client = ChemClient()

# Get a single chemical
chem = client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N")  # Using InChI key
print(f"Chemical ID: {chem.id}")
print(f"Molecular Formula: {chem.pubchem.molecular_formula}")
print(f"SMILES: {chem.pubchem.smiles}")
print(f"Molecular Weight: {chem.pubchem.molecular_weight}")
print(f"XLogP: {chem.pubchem.xlogp}")
print(f"Hydrogen Bond Donors: {chem.pubchem.hydrogen_bond_donor_count}")
print(f"Hydrogen Bond Acceptors: {chem.pubchem.hydrogen_bond_acceptor_count}")
print(f"Rotatable Bonds: {chem.pubchem.rotatable_bond_count}")
print(f"Topological Polar Surface Area: {chem.pubchem.topological_polar_surface_area} Å²")

# Get multiple chemicals
chems = client.getchems(["ZRALSGWEFCBTJO-UHFFFAOYSA-N", "RRUDCFGSUDOHDG-UHFFFAOYSA-N"])
for chem in chems:
    print(f"\nFound chemical: {chem.id}")
    if chem.has_pubchem():
        print(f"Molecular Formula: {chem.pubchem.molecular_formula}")
        print(f"Molecular Weight: {chem.pubchem.molecular_weight}")

# Query chemicals with different field filters
print("\n=== Simple Queries ===")
results = client.query("pubchem.molecular_formula:C6H12O6", size=5)
for hit in results["hits"]:
    print(f"Found chemical: {hit['_id']}")

print("\n=== Fielded Queries ===")
results = client.query("pubchem.molecular_weight:[100 TO 200]", size=5)
for hit in results["hits"]:
    print(f"Found chemical: {hit['_id']}")

print("\n=== Range Queries ===")
results = client.query("pubchem.xlogp:>2", size=5)
for hit in results["hits"]:
    print(f"Found chemical: {hit['_id']}")

print("\n=== Boolean Queries ===")
results = client.query("pubchem.hydrogen_bond_donor_count:>2 AND pubchem.hydrogen_bond_acceptor_count:>4", size=5)
for hit in results["hits"]:
    print(f"Found chemical: {hit['_id']}")

# Batch query chemicals with field filtering
chems = client.querymany(
    ["C6H12O6", "C12H22O11"],
    scopes=["pubchem.molecular_formula"],
    fields=["pubchem.molecular_weight", "pubchem.xlogp", "pubchem.smiles"],
    size=1
)
for chem in chems:
    print(f"\nFound chemical: {chem['_id']}")
    if 'pubchem' in chem:
        print(f"Molecular Weight: {chem['pubchem'].get('molecular_weight')}")
        print(f"XLogP: {chem['pubchem'].get('xlogp')}")
        print(f"SMILES: {chem['pubchem'].get('smiles')}")
```

#### Asynchronous Chemical Client

```python
import asyncio
from biothings_typed_client.chem import ChemClientAsync

async def main():
    # Initialize the client
    client = ChemClientAsync()
    
    # Get a single chemical
    chem = await client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N")  # Using InChI key
    if chem:
        print(f"Chemical ID: {chem.id}")
        print(f"Has PubChem info: {chem.has_pubchem()}")
        if chem.has_pubchem():
            print(f"Molecular Formula: {chem.pubchem.molecular_formula}")
            print(f"Molecular Weight: {chem.pubchem.molecular_weight}")
            print(f"XLogP: {chem.pubchem.xlogp}")
            print(f"Hydrogen Bond Donors: {chem.pubchem.hydrogen_bond_donor_count}")
            print(f"Hydrogen Bond Acceptors: {chem.pubchem.hydrogen_bond_acceptor_count}")
            print(f"Rotatable Bonds: {chem.pubchem.rotatable_bond_count}")
            print(f"Topological Polar Surface Area: {chem.pubchem.topological_polar_surface_area} Å²")
    
    # Query chemicals with different field filters
    print("\n=== Simple Queries ===")
    results = await client.query("pubchem.molecular_formula:C6H12O6", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found chemical: {hit['_id']}")
        
    print("\n=== Fielded Queries ===")
    results = await client.query("pubchem.molecular_weight:[100 TO 200]", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found chemical: {hit['_id']}")
        
    print("\n=== Range Queries ===")
    results = await client.query("pubchem.xlogp:>2", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found chemical: {hit['_id']}")
        
    print("\n=== Boolean Queries ===")
    results = await client.query("pubchem.hydrogen_bond_donor_count:>2 AND pubchem.hydrogen_bond_acceptor_count:>4", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found chemical: {hit['_id']}")
    
    await client.close()

# Run the async code
asyncio.run(main())
```

The chemical client provides access to detailed chemical compound information from MyChem.info, including:

- **Structural Information**:
  - Molecular formula
  - SMILES strings
  - InChI and InChIKey
  - IUPAC names

- **Physical Properties**:
  - Molecular weight
  - Exact mass
  - Monoisotopic weight
  - XLogP (octanol-water partition coefficient)
  - Topological polar surface area

- **Chemical Properties**:
  - Hydrogen bond donors/acceptors
  - Rotatable bonds
  - Chiral centers
  - Formal charge
  - Molecular complexity

- **Stereochemistry**:
  - Chiral atom count
  - Chiral bond count
  - Defined/undefined stereocenters

For more information about available fields and data sources, see the [MyChem.info documentation](https://docs.mychem.info/en/latest/doc/data.html#available-fields).

### Taxon Client Examples

#### Synchronous Taxon Client

```python
from biothings_typed_client.taxons import TaxonClient

# Initialize the client
client = TaxonClient()

# Get a single taxon
taxon = client.gettaxon(9606)  # Using taxon ID for Homo sapiens
if taxon:
    print(f"Taxon ID: {taxon.id}")
    print(f"Scientific Name: {taxon.scientific_name}")
    print(f"Common Name: {taxon.common_name}")

# Get multiple taxa
taxa = client.gettaxons([9606, 10090])  # Homo sapiens and Mus musculus
for taxon in taxa:
    print(f"Found taxon: {taxon.scientific_name}")

# Query taxa
results = client.query("scientific_name:Homo sapiens", size=5)
for hit in results["hits"]:
    print(f"Found taxon: {hit['scientific_name']}")

# Batch query taxa
taxa = client.querymany(["Homo sapiens", "Mus musculus"], scopes=["scientific_name"], size=1)
for taxon in taxa:
    print(f"Found taxon: {taxon['scientific_name']}")
```

#### Asynchronous Taxon Client

```python
import asyncio
from biothings_typed_client.taxons import TaxonClientAsync

async def main():
    # Initialize the client
    client = TaxonClientAsync()
    
    # Get a single taxon
    taxon = await client.gettaxon(9606)  # Using taxon ID for Homo sapiens
    if taxon:
        print(f"Taxon ID: {taxon.id}")
        print(f"Has lineage: {taxon.has_lineage()}")
        print(f"Has common name: {taxon.has_common_name()}")
    
    # Query taxa
    results = await client.query("scientific_name:Homo sapiens", size=5)
    print("\nQuery results:")
    for hit in results["hits"]:
        print(f"Found taxon: {hit['scientific_name']}")

# Run the async code
asyncio.run(main())
```

### Variant Client Examples

#### Synchronous Variant Client

```python
from biothings_typed_client.variants import VariantClient

# Initialize the client
client = VariantClient()

# Get a single variant
variant = client.getvariant("chr7:g.140453134T>C")
if variant:
    print(f"Variant ID: {variant.get_variant_id()}")
    print(f"Has clinical significance: {variant.has_clinical_significance()}")
    print(f"Variant details: {variant.model_dump_json(indent=2)}")
else:
    print("Variant not found")

# Query variants using different syntax
print("\n=== Simple Queries ===")
results = client.query("rs58991260")
print(f"Query 'rs58991260' results: {results['total']} hits")
if results['hits']:
    print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
    print(f"Score: {results['hits'][0].get('_score', 'No score')}")

print("\n=== Fielded Queries ===")
results = client.query("dbsnp.vartype:snp")
print(f"Query 'dbsnp.vartype:snp' results: {results['total']} hits")
if results['hits']:
    print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
    print(f"Score: {results['hits'][0].get('_score', 'No score')}")

print("\n=== Range Queries ===")
results = client.query("dbnsfp.polyphen2.hdiv.score:>0.99")
print(f"Query 'dbnsfp.polyphen2.hdiv.score:>0.99' results: {results['total']} hits")
if results['hits']:
    print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
    print(f"Score: {results['hits'][0].get('_score', 'No score')}")

print("\n=== Wildcard Queries ===")
results = client.query("dbnsfp.genename:CDK?")
print(f"Query 'dbnsfp.genename:CDK?' results: {results['total']} hits")
if results['hits']:
    print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
    print(f"Score: {results['hits'][0].get('_score', 'No score')}")

print("\n=== Boolean Queries ===")
results = client.query("_exists_:dbsnp AND dbsnp.vartype:snp")
print(f"Query '_exists_:dbsnp AND dbsnp.vartype:snp' results: {results['total']} hits")
if results['hits']:
    print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
    print(f"Score: {results['hits'][0].get('_score', 'No score')}")
```

#### Asynchronous Variant Client

```python
import asyncio
from biothings_typed_client.variants import VariantClientAsync

async def main():
    client = VariantClientAsync()
    
    # Get a single variant
    variant = await client.getvariant("chr7:g.140453134T>C")
    if variant:
        print(f"Variant ID: {variant.get_variant_id()}")
        print(f"Has clinical significance: {variant.has_clinical_significance()}")
        print(f"Variant details: {variant.model_dump_json(indent=2)}")
    else:
        print("Variant not found")
        
    # Query variants using different syntax
    print("\n=== Simple Queries ===")
    results = await client.query("rs58991260")
    print(f"Query 'rs58991260' results: {results['total']} hits")
    if results['hits']:
        print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
        print(f"Score: {results['hits'][0].get('_score', 'No score')}")
        
    print("\n=== Fielded Queries ===")
    results = await client.query("dbsnp.vartype:snp")
    print(f"Query 'dbsnp.vartype:snp' results: {results['total']} hits")
    if results['hits']:
        print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
        print(f"Score: {results['hits'][0].get('_score', 'No score')}")
        
    print("\n=== Range Queries ===")
    results = await client.query("dbnsfp.polyphen2.hdiv.score:>0.99")
    print(f"Query 'dbnsfp.polyphen2.hdiv.score:>0.99' results: {results['total']} hits")
    if results['hits']:
        print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
        print(f"Score: {results['hits'][0].get('_score', 'No score')}")
        
    print("\n=== Wildcard Queries ===")
    results = await client.query("dbnsfp.genename:CDK?")
    print(f"Query 'dbnsfp.genename:CDK?' results: {results['total']} hits")
    if results['hits']:
        print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
        print(f"Score: {results['hits'][0].get('_score', 'No score')}")
        
    print("\n=== Boolean Queries ===")
    results = await client.query("_exists_:dbsnp AND dbsnp.vartype:snp")
    print(f"Query '_exists_:dbsnp AND dbsnp.vartype:snp' results: {results['total']} hits")
    if results['hits']:
        print(f"First result: {results['hits'][0].get('_id', 'No ID')}")
        print(f"Score: {results['hits'][0].get('_score', 'No score')}")
    
    await client.close()

# Run the async code
asyncio.run(main())
```

## Available Clients

The library currently provides the following typed clients:

- `VariantClient` / `VariantClientAsync`: For accessing variant data
- `GeneClient` / `GeneClientAsync`: For accessing gene data
- `ChemClient` / `ChemClientAsync`: For accessing chemical compound data
- `TaxonClient` / `TaxonClientAsync`: For accessing taxonomic information
- More clients coming soon...

## Response Models

The library provides strongly-typed response models for all data types. For example, the `VariantResponse` model includes:

```python
class VariantResponse(BaseModel):
    id: str = Field(description="Variant identifier")
    version: int = Field(description="Version number")
    chrom: str = Field(description="Chromosome number")
    hg19: GenomicLocation = Field(description="HG19 genomic location")
    vcf: VCFInfo = Field(description="VCF information")
    
    # Optional annotation fields
    cadd: Optional[CADDScore] = None
    clinvar: Optional[ClinVarAnnotation] = None
    cosmic: Optional[CosmicAnnotation] = None
    dbnsfp: Optional[DbNSFPPrediction] = None
    dbsnp: Optional[DbSNPAnnotation] = None
    # ... and more
```

## Helper Methods

The response models include useful helper methods:

```python
# Get a standardized variant ID
variant.get_variant_id()

# Check for clinical significance
variant.has_clinical_significance()

# Check for functional predictions
variant.has_functional_predictions()
```

## Development

### Running Tests

```bash
uv run pytest -vvv
```
You can add -s to also get stdout

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BioThings](https://biothings.io/) for the biothings API and original [client library](https://github.com/biothings/biothings_client.py)

- This project is part of the [Longevity Genie](https://github.com/longevity-genie) organization, which develops open-source AI assistants and libraries for health, genetics, and longevity research.

We are supported by:

[![HEALES](images/heales.jpg)](https://heales.org/)

*HEALES - Healthy Life Extension Society*

and

[![IBIMA](images/IBIMA.jpg)](https://ibima.med.uni-rostock.de/)

[IBIMA - Institute for Biostatistics and Informatics in Medicine and Ageing Research](https://ibima.med.uni-rostock.de/)