from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .abstract_client import AbstractClient, AbstractClientAsync

if TYPE_CHECKING:
    import pandas as pd

class RefSeq(BaseModel):
    """RefSeq information for a gene"""
    genomic: Optional[List[str]] = Field(default=None, description="Genomic RefSeq IDs")
    protein: Optional[Union[str, List[str]]] = Field(default=None, description="Protein RefSeq IDs")
    rna: Optional[Union[str, List[str]]] = Field(default=None, description="RNA RefSeq IDs")
    translation: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = Field(default=None, description="Protein-RNA translation pairs")

    @field_validator('protein', 'rna', mode='before')
    @classmethod
    def ensure_list(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [v]
        return v

    @field_validator('translation', mode='before')
    @classmethod
    def ensure_translation_list(cls, v):
        if v is None:
            return None
        if isinstance(v, dict):
            return [v]
        return v

class GeneResponse(BaseModel):
    """Response model for gene information"""
    model_config = ConfigDict(extra='allow')
    
    id: str = Field(description="Gene identifier", validation_alias="_id")
    score: Optional[float] = Field(default=None, description="Search score", validation_alias="_score")
    name: Optional[str] = Field(default=None, description="Gene name")
    symbol: Optional[str] = Field(default=None, description="Gene symbol")
    refseq: Optional[RefSeq] = Field(default=None, description="RefSeq information")
    taxid: Optional[int] = Field(default=None, description="Taxonomy ID")
    entrezgene: Optional[int] = Field(default=None, description="Entrez Gene ID")
    ensembl: Optional[Dict[str, Any]] = Field(default=None, description="Ensembl information")
    uniprot: Optional[Dict[str, Any]] = Field(default=None, description="UniProt information")
    summary: Optional[str] = Field(default=None, description="Gene summary")
    genomic_pos: Optional[Dict[str, Any]] = Field(default=None, description="Genomic position information")

    def get_gene_id(self) -> str:
        """Get the gene identifier"""
        return self.id

    def has_refseq(self) -> bool:
        """Check if the gene has RefSeq information"""
        return self.refseq is not None

    def has_ensembl(self) -> bool:
        """Check if the gene has Ensembl information"""
        return self.ensembl is not None

class GeneClient(AbstractClient[GeneResponse]):
    """A typed wrapper around the BioThings gene client (synchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("gene", caching=caching)
        
    def _response_model(self) -> type[GeneResponse]:
        return GeneResponse

    def getgene(
        self,
        gene_id: Union[str, int],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[GeneResponse]:
        """
        Get gene information by ID
        
        Args:
            gene_id: The gene identifier (e.g. 1017 or "1017")
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GeneResponse object containing the gene information or None if not found
        """
        result = self._client.getgene(gene_id, fields=fields, **kwargs)
        if result is None:
            return None
        return GeneResponse.model_validate(result)
        
    def getgenes(
        self,
        gene_ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[GeneResponse]:
        """
        Get information for multiple genes
        
        Args:
            gene_ids: List of gene identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GeneResponse objects
        """
        if isinstance(gene_ids, str):
            gene_ids = gene_ids.split(",")
        elif isinstance(gene_ids, tuple):
            gene_ids = list(gene_ids)
            
        results = self._client.getgenes(gene_ids, fields=fields, **kwargs)
        return [GeneResponse.model_validate(result) for result in results]

class GeneClientAsync(AbstractClientAsync[GeneResponse]):
    """A typed wrapper around the BioThings gene client (asynchronous)"""
    
    def __init__(self, caching: bool = True):
        super().__init__("gene", caching=caching)
        
    def _response_model(self) -> type[GeneResponse]:
        return GeneResponse

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
        if not self._closed and hasattr(self._client, 'close'):
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, create a task to close the client
                    loop.create_task(self._client.close())
                else:
                    # If loop is not running, run the close operation
                    loop.run_until_complete(self._client.close())
            except Exception:
                # Ignore any errors during cleanup
                pass
            finally:
                self._closed = True
            
    async def getgene(
        self,
        gene_id: Union[str, int],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[GeneResponse]:
        """
        Get gene information by ID
        
        Args:
            gene_id: The gene identifier (e.g. 1017 or "1017")
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GeneResponse object containing the gene information or None if not found
        """
        result = await self._client.getgene(gene_id, fields=fields, **kwargs)
        if result is None:
            return None
        return GeneResponse.model_validate(result)
        
    async def getgenes(
        self,
        gene_ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[GeneResponse]:
        """
        Get information for multiple genes
        
        Args:
            gene_ids: List of gene identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GeneResponse objects
        """
        if isinstance(gene_ids, str):
            gene_ids = gene_ids.split(",")
        elif isinstance(gene_ids, tuple):
            gene_ids = list(gene_ids)
            
        results = await self._client.getgenes(gene_ids, fields=fields, **kwargs)
        return [GeneResponse.model_validate(result) for result in results]
