import logging
import pytest
import pytest_asyncio
from typing import List, Optional
from biothings_typed_client.genes import GeneClient, GeneClientAsync, GeneResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest.fixture
def sync_client():
    """Fixture providing a synchronous gene client"""
    return GeneClient()

@pytest_asyncio.fixture
async def async_client():
    async with GeneClientAsync() as client:
        yield client

def test_getgene_sync(sync_client: GeneClient):
    """Test synchronous gene retrieval"""
    gene = sync_client.getgene("672")
    assert gene is not None
    assert isinstance(gene, GeneResponse)
    assert gene.id == "672"
    assert gene.symbol == "BRCA1"
    assert gene.name is not None

def test_getgene_sync_with_fields(sync_client: GeneClient):
    """Test synchronous gene retrieval with specific fields"""
    gene = sync_client.getgene("672", fields=["symbol", "name"])
    assert gene is not None
    assert isinstance(gene, GeneResponse)
    assert gene.id == "672"
    assert gene.symbol == "BRCA1"
    assert gene.name is not None
    assert gene.refseq is None  # Not requested

def test_getgenes_sync(sync_client: GeneClient):
    """Test synchronous multiple gene retrieval"""
    genes = sync_client.getgenes(["672", "675"])
    assert len(genes) == 2
    assert all(isinstance(gene, GeneResponse) for gene in genes)
    assert genes[0].id == "672"
    assert genes[1].id == "675"

def test_query_sync(sync_client: GeneClient):
    """Test synchronous gene query"""
    results = sync_client.query("symbol:CDK2", size=1)
    assert results is not None
    assert "hits" in results
    assert len(results["hits"]) > 0
    # Convert hits to GeneResponse objects
    hits = [GeneResponse.model_validate(hit) for hit in results["hits"]]
    assert all(isinstance(hit, GeneResponse) for hit in hits)

def test_querymany_sync(sync_client: GeneClient):
    """Test synchronous batch gene query"""
    results = sync_client.querymany(["CDK2", "BRCA1"], scopes=["symbol"], size=1)
    # Convert results to GeneResponse objects
    genes = [GeneResponse.model_validate(result) for result in results]
    assert len(genes) == 2
    assert all(isinstance(gene, GeneResponse) for gene in genes)

def test_metadata_sync(sync_client: GeneClient):
    """Test synchronous metadata retrieval"""
    metadata = sync_client.metadata()
    assert metadata is not None
    assert "stats" in metadata
    assert "total" in metadata["stats"]

def test_getgene_sync_ensembl_string_refseq(sync_client: GeneClient):
    """Test sync gene retrieval for Ensembl ID with single string RefSeq genomic ID."""
    ensembl_id = "ENSECAG00000002212" # Known to return string for refseq.genomic
    gene = sync_client.getgene(ensembl_id)
    assert gene is not None
    assert isinstance(gene, GeneResponse)
    assert gene.id == "100050481" # MyGene resolves this Ensembl to Entrez ID
    assert gene.taxid == 9796 # Cavia porcellus
    assert gene.has_refseq()
    assert isinstance(gene.refseq.genomic, list) # Validator should ensure it's a list
    assert "NC_091700.1" in gene.refseq.genomic
