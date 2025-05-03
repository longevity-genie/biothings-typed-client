from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict, field_validator
from biothings_client import get_client, get_async_client
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
    
    def __init__(self):
        super().__init__("gene")
        
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

    def query(
        self,
        q: str,
        fields: Optional[Union[List[str], str]] = None,
        size: int = 10,
        skip: int = 0,
        sort: Optional[str] = None,
        species: Optional[Union[List[str], str]] = None,
        email: Optional[str] = None,
        as_dataframe: bool = False,
        df_index: bool = True,
        **kwargs
    ) -> Union[Dict[str, Any], 'pd.DataFrame']:
        """
        Query genes
        
        Args:
            q: Query string
            fields: Specific fields to return
            size: Maximum number of results to return (max 1000)
            skip: Number of results to skip
            sort: Sort field, prefix with '-' for descending order
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Query results as a dictionary or pandas DataFrame
        """
        return self._client.query(
            q,
            fields=fields,
            size=size,
            skip=skip,
            sort=sort,
            species=species,
            email=email,
            as_dataframe=as_dataframe,
            df_index=df_index,
            **kwargs
        )

    def querymany(
        self,
        query_list: Union[str, List[str], tuple],
        scopes: Optional[Union[List[str], str]] = None,
        fields: Optional[Union[List[str], str]] = None,
        species: Optional[Union[List[str], str]] = None,
        email: Optional[str] = None,
        as_dataframe: bool = False,
        df_index: bool = True,
        **kwargs
    ) -> Union[List[Dict[str, Any]], 'pd.DataFrame']:
        """
        Query for many genes
        
        Args:
            query_list: List of query terms or comma-separated string
            scopes: Fields to search in
            fields: Fields to return
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of query results or pandas DataFrame
        """
        if isinstance(query_list, str):
            query_list = query_list.split(",")
        elif isinstance(query_list, tuple):
            query_list = list(query_list)
            
        return self._client.querymany(
            query_list,
            scopes=scopes,
            fields=fields,
            species=species,
            email=email,
            **kwargs
        )

    def get_fields(self, search_term: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available fields that can be used for queries
        
        Args:
            search_term: Optional term to filter fields
            
        Returns:
            Dictionary of available fields and their descriptions
        """
        return self._client.get_fields(search_term)

    def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the gene database
        
        Returns:
            Dictionary containing database metadata
        """
        return self._client.metadata()

class GeneClientAsync(AbstractClientAsync[GeneResponse]):
    """A typed wrapper around the BioThings gene client (asynchronous)"""
    
    def __init__(self):
        super().__init__("gene")
        
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

    async def query(
        self,
        q: str,
        fields: Optional[Union[List[str], str]] = None,
        size: int = 10,
        skip: int = 0,
        sort: Optional[str] = None,
        species: Optional[Union[List[str], str]] = None,
        email: Optional[str] = None,
        as_dataframe: bool = False,
        df_index: bool = True,
        **kwargs
    ) -> Union[Dict[str, Any], 'pd.DataFrame']:
        """
        Query genes
        
        Args:
            q: Query string
            fields: Specific fields to return
            size: Maximum number of results to return (max 1000)
            skip: Number of results to skip
            sort: Sort field, prefix with '-' for descending order
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Query results as a dictionary or pandas DataFrame
        """
        return await self._client.query(
            q,
            fields=fields,
            size=size,
            skip=skip,
            sort=sort,
            species=species,
            email=email,
            as_dataframe=as_dataframe,
            df_index=df_index,
            **kwargs
        )

    async def querymany(
        self,
        query_list: Union[str, List[str], tuple],
        scopes: Optional[Union[List[str], str]] = None,
        fields: Optional[Union[List[str], str]] = None,
        species: Optional[Union[List[str], str]] = None,
        email: Optional[str] = None,
        as_dataframe: bool = False,
        df_index: bool = True,
        **kwargs
    ) -> Union[List[Dict[str, Any]], 'pd.DataFrame']:
        """
        Query for many genes
        
        Args:
            query_list: List of query terms or comma-separated string
            scopes: Fields to search in
            fields: Fields to return
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of query results or pandas DataFrame
        """
        if isinstance(query_list, str):
            query_list = query_list.split(",")
        elif isinstance(query_list, tuple):
            query_list = list(query_list)
            
        return await self._client.querymany(
            query_list,
            scopes=scopes,
            fields=fields,
            species=species,
            email=email,
            **kwargs
        )

    async def get_fields(self, search_term: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available fields that can be used for queries
        
        Args:
            search_term: Optional term to filter fields
            
        Returns:
            Dictionary of available fields and their descriptions
        """
        return await self._client.get_fields(search_term)

    async def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the gene database
        
        Returns:
            Dictionary containing database metadata
        """
        return await self._client.metadata()

if __name__ == "__main__":
    # Example usage for sync client
    client = GeneClient()
    gene = client.getgene(1017, fields="name,symbol,refseq")
    if gene:
        print(f"Gene ID: {gene.get_gene_id()}")
        print(f"Has RefSeq: {gene.has_refseq()}")
        print(f"Has Ensembl: {gene.has_ensembl()}")
        print("\nFull gene data:")
        print(gene.model_dump_json(indent=2))
    
    # Example usage for async client
    import asyncio
    
    async def main():
        client = GeneClientAsync()
        gene = await client.getgene(1017, fields="name,symbol,refseq")
        if gene:
            print(f"Gene ID: {gene.get_gene_id()}")
            print(f"Has RefSeq: {gene.has_refseq()}")
            print(f"Has Ensembl: {gene.has_ensembl()}")
            print("\nFull gene data:")
            print(gene.model_dump_json(indent=2))
        
        # Example query
        results = await client.query("symbol:cdk2", size=5)
        print("\nQuery results:")
        print(results)
        
    asyncio.run(main())
