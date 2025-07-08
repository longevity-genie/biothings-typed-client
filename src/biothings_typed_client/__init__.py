import typer
from typing import Optional, List
import json
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from biothings_typed_client.genes import GeneClient
from biothings_typed_client.chem import ChemClient
from biothings_typed_client.variants import VariantClient
from biothings_typed_client.genesets import GenesetClient
from biothings_typed_client.taxons import TaxonClient

app = typer.Typer(
    name="biothings-typed-client",
    help="A strongly-typed Python wrapper around the BioThings Client library",
    rich_markup_mode="rich",
    no_args_is_help=True
)

console = Console()

# Gene commands
gene_app = typer.Typer(name="gene", help="Gene-related commands using MyGene.info")
app.add_typer(gene_app, name="gene")

@gene_app.command("get")
def get_gene(
    gene_id: str = typer.Argument(..., help="Gene identifier (Entrez ID or Ensembl ID)"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get gene information by ID"""
    client = GeneClient(caching=caching)
    
    fields_list = fields.split(",") if fields else None
    result = client.getgene(gene_id, fields=fields_list)
    
    if result is None:
        rprint(f"[red]Gene {gene_id} not found[/red]")
        sys.exit(1)
    
    if output_format == "json":
        rprint(json.dumps(result.model_dump(), indent=2))
    else:
        table = Table(title=f"Gene Information: {gene_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", result.id)
        if result.symbol:
            table.add_row("Symbol", result.symbol)
        if result.name:
            table.add_row("Name", result.name)
        if result.entrezgene:
            table.add_row("Entrez Gene", str(result.entrezgene))
        if result.taxid:
            table.add_row("Taxonomy ID", str(result.taxid))
        if result.summary:
            table.add_row("Summary", result.summary[:100] + "..." if len(result.summary) > 100 else result.summary)
        
        console.print(table)

@gene_app.command("list")
def get_genes(
    gene_ids: str = typer.Argument(..., help="Comma-separated list of gene identifiers"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get information for multiple genes"""
    client = GeneClient(caching=caching)
    
    gene_id_list = gene_ids.split(",")
    fields_list = fields.split(",") if fields else None
    results = client.getgenes(gene_id_list, fields=fields_list)
    
    if output_format == "json":
        rprint(json.dumps([result.model_dump() for result in results], indent=2))
    else:
        table = Table(title="Gene Information")
        table.add_column("ID", style="cyan")
        table.add_column("Symbol", style="green")
        table.add_column("Name", style="blue")
        table.add_column("Entrez Gene", style="yellow")
        
        for result in results:
            table.add_row(
                result.id,
                result.symbol or "N/A",
                result.name or "N/A",
                str(result.entrezgene) if result.entrezgene else "N/A"
            )
        
        console.print(table)

# Chem commands
chem_app = typer.Typer(name="chem", help="Chemical compound commands using MyChem.info")
app.add_typer(chem_app, name="chem")

@chem_app.command("get")
def get_chem(
    chem_id: str = typer.Argument(..., help="Chemical identifier (InChI Key)"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get chemical compound information by ID"""
    client = ChemClient(caching=caching)
    
    fields_list = fields.split(",") if fields else None
    result = client.getchem(chem_id, fields=fields_list)
    
    if result is None:
        rprint(f"[red]Chemical compound {chem_id} not found[/red]")
        sys.exit(1)
    
    if output_format == "json":
        rprint(json.dumps(result.model_dump(), indent=2))
    else:
        table = Table(title=f"Chemical Information: {chem_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", result.id)
        table.add_row("Version", str(result.version))
        
        if result.pubchem:
            if result.pubchem.molecular_formula:
                table.add_row("Molecular Formula", result.pubchem.molecular_formula)
            if result.pubchem.molecular_weight:
                table.add_row("Molecular Weight", str(result.pubchem.molecular_weight))
            if result.pubchem.cid:
                table.add_row("PubChem CID", str(result.pubchem.cid))
            if result.pubchem.inchi_key:
                table.add_row("InChI Key", result.pubchem.inchi_key)
        
        console.print(table)

@chem_app.command("list")
def get_chems(
    chem_ids: str = typer.Argument(..., help="Comma-separated list of chemical identifiers"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get information for multiple chemical compounds"""
    client = ChemClient(caching=caching)
    
    chem_id_list = chem_ids.split(",")
    fields_list = fields.split(",") if fields else None
    results = client.getchems(chem_id_list, fields=fields_list)
    
    if output_format == "json":
        rprint(json.dumps([result.model_dump() for result in results], indent=2))
    else:
        table = Table(title="Chemical Information")
        table.add_column("ID", style="cyan")
        table.add_column("Formula", style="green")
        table.add_column("Molecular Weight", style="blue")
        table.add_column("PubChem CID", style="yellow")
        
        for result in results:
            formula = result.pubchem.molecular_formula if result.pubchem else "N/A"
            weight = str(result.pubchem.molecular_weight) if result.pubchem and result.pubchem.molecular_weight else "N/A"
            cid = str(result.pubchem.cid) if result.pubchem and result.pubchem.cid else "N/A"
            
            table.add_row(result.id, formula, weight, cid)
        
        console.print(table)

# Variant commands
variant_app = typer.Typer(name="variant", help="Variant commands using MyVariant.info")
app.add_typer(variant_app, name="variant")

@variant_app.command("get")
def get_variant(
    variant_id: str = typer.Argument(..., help="Variant identifier"),
    fields: Optional[str] = typer.Option("all", "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get variant information by ID"""
    client = VariantClient(caching=caching)
    
    fields_list = fields.split(",") if fields and fields != "all" else fields
    result = client.getvariant(variant_id, fields=fields_list)
    
    if result is None:
        rprint(f"[red]Variant {variant_id} not found[/red]")
        sys.exit(1)
    
    if output_format == "json":
        rprint(json.dumps(result.model_dump(), indent=2))
    else:
        table = Table(title=f"Variant Information: {variant_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", result.id)
        table.add_row("Chromosome", result.chrom)
        table.add_row("Position", result.vcf.position)
        table.add_row("Reference", result.vcf.ref)
        table.add_row("Alternative", result.vcf.alt)
        
        if result.has_clinical_significance():
            table.add_row("Clinical Significance", "Available")
        
        console.print(table)

@variant_app.command("list")
def get_variants(
    variant_ids: str = typer.Argument(..., help="Comma-separated list of variant identifiers"),
    fields: Optional[str] = typer.Option("all", "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get information for multiple variants"""
    client = VariantClient(caching=caching)
    
    variant_id_list = variant_ids.split(",")
    fields_list = fields.split(",") if fields and fields != "all" else fields
    results = client.getvariants(variant_id_list, fields=fields_list)
    
    if output_format == "json":
        rprint(json.dumps([result.model_dump() for result in results], indent=2))
    else:
        table = Table(title="Variant Information")
        table.add_column("ID", style="cyan")
        table.add_column("Chromosome", style="green")
        table.add_column("Position", style="blue")
        table.add_column("Ref>Alt", style="yellow")
        
        for result in results:
            ref_alt = f"{result.vcf.ref}>{result.vcf.alt}"
            table.add_row(result.id, result.chrom, result.vcf.position, ref_alt)
        
        console.print(table)

# Geneset commands
geneset_app = typer.Typer(name="geneset", help="Geneset commands using MyGeneset.info")
app.add_typer(geneset_app, name="geneset")

@geneset_app.command("get")
def get_geneset(
    geneset_id: str = typer.Argument(..., help="Geneset identifier"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get geneset information by ID"""
    client = GenesetClient(caching=caching)
    
    fields_list = fields.split(",") if fields else None
    result = client.getgeneset(geneset_id, fields=fields_list)
    
    if result is None:
        rprint(f"[red]Geneset {geneset_id} not found[/red]")
        sys.exit(1)
    
    if output_format == "json":
        rprint(json.dumps(result.model_dump(), indent=2))
    else:
        table = Table(title=f"Geneset Information: {geneset_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", result.id)
        table.add_row("Name", result.name)
        table.add_row("Source", result.source)
        table.add_row("Taxonomy ID", result.taxid)
        table.add_row("Gene Count", str(result.count))
        
        if result.description:
            table.add_row("Description", result.description[:100] + "..." if len(result.description) > 100 else result.description)
        
        console.print(table)

@geneset_app.command("list")
def get_genesets(
    geneset_ids: str = typer.Argument(..., help="Comma-separated list of geneset identifiers"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get information for multiple genesets"""
    client = GenesetClient(caching=caching)
    
    geneset_id_list = geneset_ids.split(",")
    fields_list = fields.split(",") if fields else None
    results = client.getgenesets(geneset_id_list, fields=fields_list)
    
    if output_format == "json":
        rprint(json.dumps([result.model_dump() for result in results], indent=2))
    else:
        table = Table(title="Geneset Information")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Source", style="blue")
        table.add_column("Gene Count", style="yellow")
        
        for result in results:
            table.add_row(result.id, result.name, result.source, str(result.count))
        
        console.print(table)

# Taxon commands
taxon_app = typer.Typer(name="taxon", help="Taxon commands using MyTaxon.info")
app.add_typer(taxon_app, name="taxon")

@taxon_app.command("get")
def get_taxon(
    taxon_id: str = typer.Argument(..., help="Taxon identifier"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get taxon information by ID"""
    client = TaxonClient(caching=caching)
    
    fields_list = fields.split(",") if fields else None
    result = client.gettaxon(taxon_id, fields=fields_list)
    
    if result is None:
        rprint(f"[red]Taxon {taxon_id} not found[/red]")
        sys.exit(1)
    
    if output_format == "json":
        rprint(json.dumps(result.model_dump(), indent=2))
    else:
        table = Table(title=f"Taxon Information: {taxon_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("ID", result.id)
        if result.scientific_name:
            table.add_row("Scientific Name", result.scientific_name)
        if result.common_name:
            table.add_row("Common Name", result.common_name)
        if result.rank:
            table.add_row("Rank", result.rank)
        if result.taxid:
            table.add_row("Taxonomy ID", str(result.taxid))
        if result.parent_taxid:
            table.add_row("Parent Taxon ID", str(result.parent_taxid))
        
        console.print(table)

@taxon_app.command("list")
def get_taxons(
    taxon_ids: str = typer.Argument(..., help="Comma-separated list of taxon identifiers"),
    fields: Optional[str] = typer.Option(None, "--fields", "-f", help="Comma-separated list of fields to return"),
    output_format: str = typer.Option("table", "--format", help="Output format: table, json"),
    caching: bool = typer.Option(False, "--cache", help="Enable caching")
):
    """Get information for multiple taxons"""
    client = TaxonClient(caching=caching)
    
    taxon_id_list = taxon_ids.split(",")
    fields_list = fields.split(",") if fields else None
    results = client.gettaxons(taxon_id_list, fields=fields_list)
    
    if output_format == "json":
        rprint(json.dumps([result.model_dump() for result in results], indent=2))
    else:
        table = Table(title="Taxon Information")
        table.add_column("ID", style="cyan")
        table.add_column("Scientific Name", style="green")
        table.add_column("Common Name", style="blue")
        table.add_column("Rank", style="yellow")
        
        for result in results:
            table.add_row(
                result.id,
                result.scientific_name or "N/A",
                result.common_name or "N/A",
                result.rank or "N/A"
            )
        
        console.print(table)

def main() -> None:
    """Main CLI entry point"""
    app() 