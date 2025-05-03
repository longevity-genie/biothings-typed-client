# BioThings Typed Client

A strongly-typed Python wrapper around the [BioThings Client](https://github.com/biothings/biothings_client.py) library, providing type safety and better IDE support through Python's type hints and Pydantic models.

## Features

- **Type Safety**: Strongly typed models for all BioThings data using Pydantic
- **IDE Support**: Full autocompletion and type checking in modern IDEs
- **Synchronous & Asynchronous**: Support for both sync and async operations
- **Helper Methods**: Additional utility methods for common operations
- **Validation**: Runtime type checking and data validation
- **Compatibility**: Maintains full compatibility with the original BioThings client

## Installation

### Using pip

```bash
pip install biothings-typed-client
```

### Using UV (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and pip-tools.

1. Install UV (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install the package:
   ```bash
   uv sync
   ```

3. To create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   uv install biothings-typed-client
   ```

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

## Available Clients

The library currently provides the following typed clients:

- `VariantClient` / `VariantClientAsync`: For accessing variant data
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
pytest tests/
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BioThings](https://biothings.io/) for the original client library
- [Pydantic](https://pydantic-docs.helpmanual.io/) for the data validation framework
