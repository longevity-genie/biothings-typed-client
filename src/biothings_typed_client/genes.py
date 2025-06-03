from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict, field_validator
from biothings_typed_client.abstract_client import AbstractClient, AbstractClientAsync

if TYPE_CHECKING:
    import pandas as pd

class RefSeq(BaseModel):
    """RefSeq information for a gene"""
    genomic: Optional[Union[str, List[str]]] = Field(default=None, description="Genomic RefSeq IDs")
    protein: Optional[Union[str, List[str]]] = Field(default=None, description="Protein RefSeq IDs")
    rna: Optional[Union[str, List[str]]] = Field(default=None, description="RNA RefSeq IDs")
    translation: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = Field(default=None, description="Protein-RNA translation pairs")

    @field_validator('genomic', 'protein', 'rna', mode='before')
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
    """A typed wrapper around the BioThings gene client (synchronous)
    
    This client provides access to the MyGene.info gene annotation service. It supports:
    - Single gene retrieval by ID (Entrez or Ensembl)
    - Batch gene retrieval
    - Field filtering
    - Querying genes by various criteria
    
    Examples:
        >>> client = GeneClient()
        >>> # Get a single gene by Entrez ID
        >>> gene = client.getgene("1017")
        >>> # Get a single gene by Ensembl ID
        >>> gene = client.getgene("ENSG00000123374")
        >>> # Get multiple genes
        >>> genes = client.getgenes(["1017", "1018"])
        >>> # Get specific fields
        >>> gene = client.getgene("1017", fields=["symbol", "name", "refseq.rna"])
        >>> # Query genes
        >>> results = client.query("symbol:CDK2", size=5)
        >>> # Batch query genes
        >>> genes = client.querymany(["CDK2", "BRCA1"], scopes=["symbol"], size=1)
    """
    
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
            gene_id: The gene identifier (e.g. 1017 or "1017" for Entrez ID, 
                    or "ENSG00000123374" for Ensembl ID)
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields (e.g. "refseq.rna").
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GeneResponse object containing the gene information or None if not found
            
        Examples:
            >>> # Get all fields
            >>> gene = client.getgene("1017")
            >>> # Get specific fields
            >>> gene = client.getgene("1017", fields=["symbol", "name", "refseq.rna"])
            >>> # Get fields using dot notation
            >>> gene = client.getgene("1017", fields="refseq.rna,ensembl.gene")
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
            gene_ids: List of gene identifiers or comma-separated string.
                     Can be Entrez IDs or Ensembl IDs.
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GeneResponse objects
            
        Examples:
            >>> # Get multiple genes by Entrez IDs
            >>> genes = client.getgenes(["1017", "1018"])
            >>> # Get multiple genes by Ensembl IDs
            >>> genes = client.getgenes(["ENSG00000123374", "ENSG00000139618"])
            >>> # Get specific fields
            >>> genes = client.getgenes(["1017", "1018"], fields=["symbol", "name"])
        """
        if isinstance(gene_ids, str):
            gene_ids = gene_ids.split(",")
        elif isinstance(gene_ids, tuple):
            gene_ids = list(gene_ids)
            
        results = self._client.getgenes(gene_ids, fields=fields, **kwargs)
        return [GeneResponse.model_validate(result) for result in results]

class GeneClientAsync(AbstractClientAsync[GeneResponse]):
    """A typed wrapper around the BioThings gene client (asynchronous)
    
    This client provides asynchronous access to the MyGene.info gene annotation service.
    It supports the same functionality as the synchronous client but with async/await syntax.
    
    Examples:
        >>> async with GeneClientAsync() as client:
        >>>     # Get a single gene
        >>>     gene = await client.getgene("1017")
        >>>     # Get multiple genes
        >>>     genes = await client.getgenes(["1017", "1018"])
        >>>     # Query genes
        >>>     results = await client.query("symbol:CDK2", size=5)
        >>>     # Batch query genes
        >>>     genes = await client.querymany(["CDK2", "BRCA1"], scopes=["symbol"], size=1)
    """
    
    def __init__(self, caching: bool = True):
        super().__init__("gene", caching=caching)
        
    def _response_model(self) -> type[GeneResponse]:
        return GeneResponse
            
    async def getgene(
        self,
        gene_id: Union[str, int],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[GeneResponse]:
        """
        Get gene information by ID asynchronously
        
        Args:
            gene_id: The gene identifier (e.g. 1017 or "1017" for Entrez ID, 
                    or "ENSG00000123374" for Ensembl ID)
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields (e.g. "refseq.rna").
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            GeneResponse object containing the gene information or None if not found
            
        Examples:
            >>> async with GeneClientAsync() as client:
            >>>     # Get all fields
            >>>     gene = await client.getgene("1017")
            >>>     # Get specific fields
            >>>     gene = await client.getgene("1017", fields=["symbol", "name", "refseq.rna"])
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
        Get information for multiple genes asynchronously
        
        Args:
            gene_ids: List of gene identifiers or comma-separated string.
                     Can be Entrez IDs or Ensembl IDs.
            fields: Specific fields to return. Can be a comma-separated string or list.
                   Supports dot notation for nested fields.
                   If None, returns all available fields.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of GeneResponse objects
            
        Examples:
            >>> async with GeneClientAsync() as client:
            >>>     # Get multiple genes
            >>>     genes = await client.getgenes(["1017", "1018"])
            >>>     # Get specific fields
            >>>     genes = await client.getgenes(["1017", "1018"], fields=["symbol", "name"])
        """
        if isinstance(gene_ids, str):
            gene_ids = gene_ids.split(",")
        elif isinstance(gene_ids, tuple):
            gene_ids = list(gene_ids)
            
        results = await self._client.getgenes(gene_ids, fields=fields, **kwargs)
        return [GeneResponse.model_validate(result) for result in results]