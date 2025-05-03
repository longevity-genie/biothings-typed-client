import logging
import pytest
import pytest_asyncio
from typing import List, Optional
from biothings_typed_client.variants import VariantClient, VariantClientAsync, VariantResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest.fixture
def sync_client():
    return VariantClient()

@pytest_asyncio.fixture
async def async_client():
    client = VariantClientAsync()
    yield client
    await client.close()

def test_getvariant_sync(sync_client: VariantClient):
    """Test getting a single variant using sync client"""
    variant = sync_client.getvariant("chr7:g.140453134T>C")
    assert variant is not None
    assert variant.id == "chr7:g.140453134T>C"
    assert variant.chrom == "7"
    assert variant.vcf.ref == "T"
    assert variant.vcf.alt == "C"
    assert variant.vcf.position == "140453134"
    assert variant.hg19.start == 140453134
    assert variant.hg19.end == 140453134

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

def test_getvariants_sync(sync_client: VariantClient):
    """Test getting multiple variants using sync client"""
    variants = sync_client.getvariants(["chr7:g.140453134T>C", "chr9:g.107620835G>A"])
    assert len(variants) == 2
    assert all(isinstance(v, VariantResponse) for v in variants)
    assert variants[0].id == "chr7:g.140453134T>C"
    assert variants[1].id == "chr9:g.107620835G>A"

@pytest.mark.asyncio
async def test_getvariants_async(async_client: VariantClientAsync):
    """Test getting multiple variants using async client"""
    variants = await async_client.getvariants(["chr7:g.140453134T>C", "chr9:g.107620835G>A"])
    assert len(variants) == 2
    assert all(isinstance(v, VariantResponse) for v in variants)
    assert variants[0].id == "chr7:g.140453134T>C"
    assert variants[1].id == "chr9:g.107620835G>A"

def test_query_sync(sync_client: VariantClient):
    """Test querying variants using sync client"""
    results = sync_client.query("dbnsfp.genename:cdk2", size=5)
    assert "hits" in results
    assert len(results["hits"]) == 5
    assert all("_id" in hit for hit in results["hits"])

@pytest.mark.asyncio
async def test_query_async(async_client: VariantClientAsync):
    """Test querying variants using async client"""
    results = await async_client.query("dbnsfp.genename:cdk2", size=5)
    assert "hits" in results
    assert len(results["hits"]) == 5
    assert all("_id" in hit for hit in results["hits"])

def test_querymany_sync(sync_client: VariantClient):
    """Test querying many variants using sync client"""
    results = sync_client.querymany(["rs58991260", "rs12190874"], scopes="dbsnp.rsid")
    assert len(results) == 2
    assert all("_id" in result for result in results)

@pytest.mark.asyncio
async def test_querymany_async(async_client: VariantClientAsync):
    """Test querying many variants using async client"""
    results = await async_client.querymany(["rs58991260", "rs12190874"], scopes="dbsnp.rsid")
    assert len(results) == 2
    assert all("_id" in result for result in results)

def test_get_fields_sync(sync_client: VariantClient):
    """Test getting available fields using sync client"""
    fields = sync_client.get_fields()
    assert isinstance(fields, dict)
    assert len(fields) > 0
    assert "chrom" in fields
    assert "vcf" in fields

@pytest.mark.asyncio
async def test_get_fields_async(async_client: VariantClientAsync):
    """Test getting available fields using async client"""
    fields = await async_client.get_fields()
    assert isinstance(fields, dict)
    assert len(fields) > 0
    assert "chrom" in fields
    assert "vcf" in fields

def test_metadata_sync(sync_client: VariantClient):
    """Test getting metadata using sync client"""
    metadata = sync_client.metadata()
    assert isinstance(metadata, dict)
    assert "stats" in metadata
    assert "total" in metadata["stats"]

@pytest.mark.asyncio
async def test_metadata_async(async_client: VariantClientAsync):
    """Test getting metadata using async client"""
    metadata = await async_client.metadata()
    assert isinstance(metadata, dict)
    assert "stats" in metadata
    assert "total" in metadata["stats"]
