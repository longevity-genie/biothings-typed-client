from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

try:
    from .abstract_client import AbstractClient, AbstractClientAsync
except ImportError:
    from biothings_typed_client.abstract_client import AbstractClient, AbstractClientAsync

class TaxonResponse(BaseModel):
    """Response model for taxon information"""
    model_config = ConfigDict(extra='allow')
    
    id: str = Field(description="Taxon identifier", validation_alias="_id", serialization_alias="_id")
    version: int = Field(description="Version number of the data", validation_alias="_version", serialization_alias="_version")
    authority: Optional[List[str]] = Field(default=None, description="Taxonomic authority")
    common_name: Optional[str] = Field(default=None, description="Common name")
    genbank_common_name: Optional[str] = Field(default=None, description="GenBank common name")
    has_gene: Optional[bool] = Field(default=None, description="Whether the taxon has gene data")
    lineage: Optional[List[int]] = Field(default=None, description="Taxonomic lineage IDs")
    other_names: Optional[List[str]] = Field(default=None, description="Other names")
    parent_taxid: Optional[int] = Field(default=None, description="Parent taxon ID")
    rank: Optional[str] = Field(default=None, description="Taxonomic rank")
    scientific_name: Optional[str] = Field(default=None, description="Scientific name")
    taxid: Optional[int] = Field(default=None, description="Taxon ID")
    uniprot_name: Optional[str] = Field(default=None, description="UniProt name")

    def get_taxon_id(self) -> str:
        """Get the taxon identifier"""
        return self.id

    def has_lineage(self) -> bool:
        """Check if the taxon has lineage information"""
        return self.lineage is not None and len(self.lineage) > 0

    def has_common_name(self) -> bool:
        """Check if the taxon has a common name"""
        return self.common_name is not None

class TaxonClient(AbstractClient[TaxonResponse]):
    """A typed wrapper around the BioThings taxon client (synchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("taxon", caching=caching)
        
    def _response_model(self) -> type[TaxonResponse]:
        return TaxonResponse

    def gettaxon(
        self,
        taxon_id: Union[str, int],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[TaxonResponse]:
        """
        Get taxon information by ID
        
        Args:
            taxon_id: The taxon identifier (e.g. 9606 for Homo sapiens)
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            TaxonResponse object containing the taxon information or None if not found
        """
        result = self._client.gettaxon(taxon_id, fields=fields, **kwargs)
        if result is None:
            return None
        return TaxonResponse.model_validate(result)
        
    def gettaxons(
        self,
        taxon_ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[TaxonResponse]:
        """
        Get information for multiple taxa
        
        Args:
            taxon_ids: List of taxon identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of TaxonResponse objects
        """
        if isinstance(taxon_ids, str):
            taxon_ids = taxon_ids.split(",")
        elif isinstance(taxon_ids, tuple):
            taxon_ids = list(taxon_ids)
            
        results = self._client.gettaxons(taxon_ids, fields=fields, **kwargs)
        return [TaxonResponse.model_validate(result) for result in results]

class TaxonClientAsync(AbstractClientAsync[TaxonResponse]):
    """A typed wrapper around the BioThings taxon client (asynchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("taxon", caching=caching)
        
    def _response_model(self) -> type[TaxonResponse]:
        return TaxonResponse

    async def gettaxon(
        self,
        taxon_id: Union[str, int],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[TaxonResponse]:
        """
        Get taxon information by ID
        
        Args:
            taxon_id: The taxon identifier (e.g. 9606 for Homo sapiens)
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            TaxonResponse object containing the taxon information or None if not found
        """
        result = await self._client.gettaxon(taxon_id, fields=fields, **kwargs)
        if result is None:
            return None
        return TaxonResponse.model_validate(result)
        
    async def gettaxons(
        self,
        taxon_ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[TaxonResponse]:
        """
        Get information for multiple taxa
        
        Args:
            taxon_ids: List of taxon identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of TaxonResponse objects
        """
        if isinstance(taxon_ids, str):
            taxon_ids = taxon_ids.split(",")
        elif isinstance(taxon_ids, tuple):
            taxon_ids = list(taxon_ids)
            
        results = await self._client.gettaxons(taxon_ids, fields=fields, **kwargs)
        return [TaxonResponse.model_validate(result) for result in results]