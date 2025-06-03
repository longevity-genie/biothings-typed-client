from typing import Any, Dict, List, Optional, Union, Generator
from pydantic import BaseModel, Field, ConfigDict
from biothings_typed_client.abstract_client import AbstractClient, AbstractClientAsync

class GeneInfo(BaseModel):
    """Gene information within a geneset"""
    mygene_id: Optional[str] = Field(default=None, description="MyGene.info ID")
    symbol: Optional[str] = Field(default=None, description="Gene symbol")
    name: Optional[str] = Field(default=None, description="Gene name")
    ncbigene: Optional[str] = Field(default=None, description="NCBI Gene ID")

class WikiPathwaysInfo(BaseModel):
    """WikiPathways specific information"""
    id: str = Field(description="WikiPathways ID")
    pathway_name: str = Field(description="Pathway name")
    url: str = Field(description="Pathway URL")
    _license: str = Field(description="License information")

class GenesetResponse(BaseModel):
    """Response model for geneset information"""
    model_config = ConfigDict(extra='allow')
    
    id: str = Field(description="Geneset identifier", validation_alias="_id")
    name: str = Field(description="Geneset name")
    source: str = Field(description="Source database")
    taxid: str = Field(description="Taxonomy ID")
    genes: List[GeneInfo] = Field(description="List of genes in the geneset")
    count: int = Field(description="Number of genes in the geneset")
    wikipathways: Optional[WikiPathwaysInfo] = Field(default=None, description="WikiPathways specific information")
    description: Optional[str] = Field(default=None, description="Geneset description")
    
    # Source-specific fields
    go: Optional[Dict[str, Any]] = Field(default=None, description="GO specific information")
    ctd: Optional[Dict[str, Any]] = Field(default=None, description="CTD specific information")
    msigdb: Optional[Dict[str, Any]] = Field(default=None, description="MSigDB specific information")
    do: Optional[Dict[str, Any]] = Field(default=None, description="DO specific information")
    reactome: Optional[Dict[str, Any]] = Field(default=None, description="Reactome specific information")
    smpdb: Optional[Dict[str, Any]] = Field(default=None, description="SMPDB specific information")

    def get_geneset_id(self) -> str:
        """Get the geneset identifier"""
        return self.id

    def has_wikipathways(self) -> bool:
        """Check if the geneset has WikiPathways information"""
        return self.wikipathways is not None

    def has_source_info(self, source: str) -> bool:
        """Check if the geneset has information for a specific source"""
        return getattr(self, source) is not None

class GenesetClient(AbstractClient[GenesetResponse]):
    """A typed wrapper around the BioThings geneset client (synchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("geneset", caching=caching)
        
    def _response_model(self) -> type[GenesetResponse]:
        return GenesetResponse

    def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the geneset database
        
        Returns:
            Dictionary containing metadata information
        """
        return self._client.metadata()

    def getgeneset(
        self,
        geneset_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[GenesetResponse]:
        """
        Get geneset information by ID
        
        Args:
            geneset_id: The geneset identifier (e.g. "WP100")
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields (e.g. "genes.mygene_id").
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GenesetResponse object containing the geneset information or None if not found
        """
        result = self._client.getgeneset(geneset_id, fields=fields, **kwargs)
        if result is None:
            return None
        return GenesetResponse.model_validate(result)
        
    def getgenesets(
        self,
        geneset_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[GenesetResponse]:
        """
        Get information for multiple genesets
        
        Args:
            geneset_ids: List of geneset identifiers or comma-separated string
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GenesetResponse objects
        """
        if isinstance(geneset_ids, str):
            geneset_ids = geneset_ids.split(",")
        elif isinstance(geneset_ids, tuple):
            geneset_ids = list(geneset_ids)
            
        results = self._client.getgenesets(geneset_ids, fields=fields, **kwargs)
        return [GenesetResponse.model_validate(result) for result in results]

    def query(
        self,
        q: str,
        fields: Optional[Union[List[str], str]] = None,
        size: Optional[int] = None,
        species: Optional[str] = None,
        fetch_all: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[GenesetResponse, None, None]]:
        """
        Query genesets
        
        Args:
            q: Query string
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            size: Maximum number of results to return
            species: Filter by species (taxonomy ID)
            fetch_all: If True, returns a generator that yields all results
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            If fetch_all is False, returns a dictionary with query results.
            If fetch_all is True, returns a generator that yields GenesetResponse objects.
        """
        if fetch_all:
            results = self._client.query(q, fields=fields, size=size, species=species, fetch_all=True, **kwargs)
            return (GenesetResponse.model_validate(result) for result in results)
        else:
            results = self._client.query(q, fields=fields, size=size, species=species, **kwargs)
            if "hits" in results:
                results["hits"] = [GenesetResponse.model_validate(hit) for hit in results["hits"]]
            return results

class GenesetClientAsync(AbstractClientAsync[GenesetResponse]):
    """A typed wrapper around the BioThings geneset client (asynchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("geneset", caching=caching)
        
    def _response_model(self) -> type[GenesetResponse]:
        return GenesetResponse

    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
            
    async def close(self):
        """Close the client connection"""
        if not self._closed and hasattr(self._client, 'close'):
            try:
                await self._client.close()
            except Exception:
                # Ignore any errors during cleanup
                pass
            finally:
                self._closed = True
                
    def __del__(self):
        """Cleanup when the object is deleted"""
        if not self._closed:
            # Mark as closed to prevent further cleanup attempts
            self._closed = True
            
            # Don't try to close async resources during garbage collection
            # This can cause "coroutine was never awaited" warnings
            # Proper cleanup should be done via explicit close() calls or context managers

    async def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the geneset database asynchronously
        
        Returns:
            Dictionary containing metadata information
        """
        return await self._client.metadata()

    async def getgeneset(
        self,
        geneset_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[GenesetResponse]:
        """
        Get geneset information by ID asynchronously
        
        Args:
            geneset_id: The geneset identifier (e.g. "WP100")
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields (e.g. "genes.mygene_id").
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GenesetResponse object containing the geneset information or None if not found
        """
        result = await self._client.getgeneset(geneset_id, fields=fields, **kwargs)
        if result is None:
            return None
        return GenesetResponse.model_validate(result)
        
    async def getgenesets(
        self,
        geneset_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[GenesetResponse]:
        """
        Get information for multiple genesets asynchronously
        
        Args:
            geneset_ids: List of geneset identifiers or comma-separated string
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GenesetResponse objects
        """
        if isinstance(geneset_ids, str):
            geneset_ids = geneset_ids.split(",")
        elif isinstance(geneset_ids, tuple):
            geneset_ids = list(geneset_ids)
            
        results = await self._client.getgenesets(geneset_ids, fields=fields, **kwargs)
        return [GenesetResponse.model_validate(result) for result in results]

    async def query(
        self,
        q: str,
        fields: Optional[Union[List[str], str]] = None,
        size: Optional[int] = None,
        species: Optional[str] = None,
        fetch_all: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[GenesetResponse, None, None]]:
        """
        Query genesets asynchronously
        
        Args:
            q: Query string
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            size: Maximum number of results to return
            species: Filter by species (taxonomy ID)
            fetch_all: If True, returns a generator that yields all results
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            If fetch_all is False, returns a dictionary with query results.
            If fetch_all is True, returns a generator that yields GenesetResponse objects.
        """
        if fetch_all:
            results = await self._client.query(q, fields=fields, size=size, species=species, fetch_all=True, **kwargs)
            return (GenesetResponse.model_validate(result) for result in results)
        else:
            results = await self._client.query(q, fields=fields, size=size, species=species, **kwargs)
            if "hits" in results:
                results["hits"] = [GenesetResponse.model_validate(hit) for hit in results["hits"]]
            return results
