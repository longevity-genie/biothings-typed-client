import logging
import pytest
import pytest_asyncio
from biothings_typed_client.chem import ChemClientAsync, ChemResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest_asyncio.fixture
async def async_client():
    """Fixture providing an asynchronous chem client"""
    async with ChemClientAsync() as client:
        yield client

@pytest.mark.asyncio
async def test_getchem_async(async_client: ChemClientAsync):
    """Test async chemical retrieval"""
    chem = await async_client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N")
    assert chem is not None
    assert isinstance(chem, ChemResponse)
    assert chem.id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chem.has_pubchem()

@pytest.mark.asyncio
async def test_getchem_async_with_fields(async_client: ChemClientAsync):
    """Test async chemical retrieval with specific fields"""
    chem = await async_client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N", fields=["pubchem.molecular_formula", "pubchem.cid"])
    assert chem is not None
    assert isinstance(chem, ChemResponse)
    assert chem.id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chem.pubchem is not None
    assert chem.pubchem.molecular_formula is not None
    assert chem.pubchem.cid is not None

@pytest.mark.asyncio
async def test_getchems_async(async_client: ChemClientAsync):
    """Test async multiple chemical retrieval"""
    chems = await async_client.getchems(["ZRALSGWEFCBTJO-UHFFFAOYSA-N", "RRUDCFGSUDOHDG-UHFFFAOYSA-N"])
    assert len(chems) == 2
    assert all(isinstance(chem, ChemResponse) for chem in chems)
    assert chems[0].id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chems[1].id == "RRUDCFGSUDOHDG-UHFFFAOYSA-N"

@pytest.mark.asyncio
async def test_metadata_async(async_client: ChemClientAsync):
    """Test async metadata retrieval"""
    metadata = await async_client.metadata()
    assert metadata is not None
    assert "stats" in metadata
    assert "total" in metadata["stats"]
