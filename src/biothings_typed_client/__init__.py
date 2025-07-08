import warnings

# Suppress warnings from underlying biothings_client async cleanup
# These warnings occur when the underlying AsyncBiothingClient is garbage collected
warnings.filterwarnings("ignore", 
                       message=".*coroutine 'AsyncBiothingClient.*' was never awaited.*",
                       category=RuntimeWarning)

warnings.filterwarnings("ignore", 
                       message=".*coroutine 'AsyncBiothingsClientSqlite3Cache.*' was never awaited.*",
                       category=RuntimeWarning)

# More specific pattern for the exact warning appearing in tests
warnings.filterwarnings("ignore", 
                       message="coroutine 'AsyncBiothingClient.__del__' was never awaited",
                       category=RuntimeWarning)

warnings.filterwarnings("ignore", 
                       message="coroutine 'AsyncBiothingsClientSqlite3Cache.cache_filepath' was never awaited",
                       category=RuntimeWarning)

# General catch for any biothings async warnings
warnings.filterwarnings("ignore", 
                       message=".*AsyncBiothingClient.*never awaited.*",
                       category=RuntimeWarning)

warnings.filterwarnings("ignore", 
                       message=".*AsyncBiothingsClient.*never awaited.*",
                       category=RuntimeWarning)

from biothings_typed_client.genes import GeneClient, GeneClientAsync
from biothings_typed_client.variants import VariantClient, VariantClientAsync
from biothings_typed_client.chem import ChemClient, ChemClientAsync
from biothings_typed_client.taxons import TaxonClient, TaxonClientAsync

__all__ = [
    "GeneClient", "GeneClientAsync",
    "VariantClient", "VariantClientAsync", 
    "ChemClient", "ChemClientAsync",
    "TaxonClient", "TaxonClientAsync"
] 