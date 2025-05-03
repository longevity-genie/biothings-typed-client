import logging
import pytest
from biothings_typed_client.chem import ChemClient, ChemResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@pytest.fixture
def sync_client():
    """Fixture providing a synchronous chem client"""
    return ChemClient()

def test_getchem_sync(sync_client: ChemClient):
    """Test synchronous chemical retrieval"""
    chem = sync_client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N")
    assert chem is not None
    assert isinstance(chem, ChemResponse)
    assert chem.id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chem.has_pubchem()

def test_getchem_sync_with_fields(sync_client: ChemClient):
    """Test synchronous chemical retrieval with specific fields"""
    chem = sync_client.getchem("ZRALSGWEFCBTJO-UHFFFAOYSA-N", fields=["pubchem.molecular_formula", "pubchem.cid"])
    assert chem is not None
    assert isinstance(chem, ChemResponse)
    assert chem.id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chem.pubchem is not None
    assert chem.pubchem.molecular_formula is not None
    assert chem.pubchem.cid is not None

def test_getchems_sync(sync_client: ChemClient):
    """Test synchronous multiple chemical retrieval"""
    chems = sync_client.getchems(["ZRALSGWEFCBTJO-UHFFFAOYSA-N", "RRUDCFGSUDOHDG-UHFFFAOYSA-N"])
    assert len(chems) == 2
    assert all(isinstance(chem, ChemResponse) for chem in chems)
    assert chems[0].id == "ZRALSGWEFCBTJO-UHFFFAOYSA-N"
    assert chems[1].id == "RRUDCFGSUDOHDG-UHFFFAOYSA-N"

def test_metadata_sync(sync_client: ChemClient):
    """Test synchronous metadata retrieval"""
    metadata = sync_client.metadata()
    assert metadata is not None
    assert "stats" in metadata
    assert "total" in metadata["stats"]
