import pytest
import pytest_asyncio
from biothings_typed_client.genes import GeneClientAsync, GeneResponse

@pytest_asyncio.fixture
async def async_client():
    """Fixture providing an asynchronous gene client"""
    client = GeneClientAsync()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_getgene_async(async_client: GeneClientAsync):
    """Test async gene retrieval"""
    gene = await async_client.getgene("1017")
    assert gene is not None
    assert isinstance(gene, GeneResponse)
    assert gene.id == "1017"
    assert gene.symbol == "CDK2"
    assert gene.name == "cyclin dependent kinase 2"

@pytest.mark.asyncio
async def test_getgene_async_with_fields(async_client: GeneClientAsync):
    """Test async gene retrieval with specific fields"""
    gene = await async_client.getgene("1017", fields=["symbol", "name"])
    assert gene is not None
    assert isinstance(gene, GeneResponse)
    assert gene.id == "1017"
    assert gene.symbol == "CDK2"
    assert gene.name == "cyclin dependent kinase 2"
    assert gene.refseq is None  # Not requested

@pytest.mark.asyncio
async def test_getgenes_async(async_client: GeneClientAsync):
    """Test async multiple gene retrieval"""
    genes = await async_client.getgenes(["1017", "1018"])
    assert len(genes) == 2
    assert all(isinstance(gene, GeneResponse) for gene in genes)
    assert genes[0].id == "1017"
    assert genes[1].id == "1018"

@pytest.mark.asyncio
async def test_query_async(async_client: GeneClientAsync):
    """Test async gene query"""
    results = await async_client.query("symbol:CDK2", size=1)
    assert results is not None
    assert "hits" in results
    assert len(results["hits"]) > 0
    # Convert hits to GeneResponse objects
    hits = [GeneResponse.model_validate(hit) for hit in results["hits"]]
    assert all(isinstance(hit, GeneResponse) for hit in hits)

@pytest.mark.asyncio
async def test_querymany_async(async_client: GeneClientAsync):
    """Test async batch gene query"""
    results = await async_client.querymany(["CDK2", "BRCA1"], scopes=["symbol"], size=1)
    # Convert results to GeneResponse objects
    genes = [GeneResponse.model_validate(result) for result in results]
    assert len(genes) == 2
    assert all(isinstance(gene, GeneResponse) for gene in genes)

@pytest.mark.asyncio
async def test_metadata_async(async_client: GeneClientAsync):
    """Test async metadata retrieval"""
    metadata = await async_client.metadata()
    assert metadata is not None
    assert "stats" in metadata
    assert "total" in metadata["stats"]
