import logging
import pytest
import pytest_asyncio
from biothings_typed_client.variants import VariantClientAsync, VariantResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest_asyncio.fixture
async def async_client():
    async with VariantClientAsync() as client:
        yield client

@pytest.mark.asyncio
async def test_getvariant_async(async_client: VariantClientAsync):
    """Test getting a single variant using async client"""
    variant = await async_client.getvariant("chr7:g.140453134T>C")
    assert variant is not None
    assert variant.id == "chr7:g.140453134T>C"
    assert variant.chrom == "7"
    assert variant.vcf.ref == "T"
    assert variant.vcf.alt == "C"
    assert variant.vcf.position == "140453134"
    assert variant.hg19.start == 140453134
    assert variant.hg19.end == 140453134

@pytest.mark.asyncio
async def test_getvariants_async(async_client: VariantClientAsync):
    """Test getting multiple variants using async client"""
    variants = await async_client.getvariants(["chr7:g.140453134T>C", "chr9:g.107620835G>A"])
    assert len(variants) == 2
    assert all(isinstance(v, VariantResponse) for v in variants)
    assert variants[0].chrom == "7"
    assert variants[1].chrom == "9"

@pytest.mark.asyncio
async def test_query_async(async_client: VariantClientAsync):
    """Test querying variants using async client"""
    results = await async_client.query("dbnsfp.genename:cdk2", size=5)
    assert "hits" in results
    assert len(results["hits"]) == 5
    assert all("_id" in hit for hit in results["hits"])

@pytest.mark.asyncio
async def test_querymany_async(async_client: VariantClientAsync):
    """Test querying many variants using async client"""
    results = await async_client.querymany(["rs58991260", "rs12190874"], scopes="dbsnp.rsid")
    assert len(results) == 2
    assert all("_id" in result for result in results)

@pytest.mark.asyncio
async def test_get_fields_async(async_client: VariantClientAsync):
    """Test getting available fields using async client"""
    fields = await async_client.get_fields()
    assert isinstance(fields, dict)
    assert len(fields) > 0
    assert "chrom" in fields
    assert "vcf" in fields

@pytest.mark.asyncio
async def test_metadata_async(async_client: VariantClientAsync):
    """Test getting metadata using async client"""
    metadata = await async_client.metadata()
    assert isinstance(metadata, dict)
    assert "stats" in metadata
    assert "total" in metadata["stats"]
