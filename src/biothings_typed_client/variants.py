from typing import Any, Dict, List, Optional, Union, Generator
from pydantic import BaseModel, Field, ConfigDict
from biothings_client import get_client, get_async_client
from pathlib import Path
import pandas as pd
from .abstract_client import AbstractClient, AbstractClientAsync

class VCFInfo(BaseModel):
    """VCF information for a variant"""
    alt: str = Field(description="Alternative allele")
    position: str = Field(description="Position in the chromosome")
    ref: str = Field(description="Reference allele")
    filter: Optional[str] = Field(default=None, description="VCF FILTER value")
    qual: Optional[float] = Field(default=None, description="VCF QUAL value")

class GenomicLocation(BaseModel):
    """Genomic location information"""
    end: int = Field(description="End position")
    start: int = Field(description="Start position")
    strand: Optional[int] = Field(default=1, description="Strand (1 or -1)")

class CADDScore(BaseModel):
    """CADD scores and predictions"""
    model_config = ConfigDict(extra='allow')
    
    phred: Optional[float] = Field(default=None, description="PHRED-scaled CADD score")
    raw: Optional[float] = Field(default=None, description="Raw CADD score")
    consequence: Optional[Union[str, List[str]]] = Field(default=None, description="Variant consequence")
    consdetail: Optional[Union[str, List[str]]] = Field(default=None, description="Detailed consequence")
    type: Optional[str] = Field(default=None, description="Variant type")

class ClinVarAnnotation(BaseModel):
    """ClinVar variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    rcv_accession: Optional[str] = Field(default=None, description="RCV accession number")
    clinical_significance: Optional[str] = Field(default=None, description="Clinical significance")
    review_status: Optional[str] = Field(default=None, description="Review status")
    last_evaluated: Optional[str] = Field(default=None, description="Last evaluation date")
    phenotype: Optional[List[str]] = Field(default=None, description="Associated phenotypes")
    phenotype_id: Optional[List[str]] = Field(default=None, description="Phenotype IDs")
    origin: Optional[List[str]] = Field(default=None, description="Allele origin")
    conditions: Optional[List[Dict[str, Any]]] = Field(default=None, description="Associated conditions")

class CosmicAnnotation(BaseModel):
    """COSMIC variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    cosmic_id: Optional[str] = Field(default=None, description="COSMIC variant ID")
    tumor_site: Optional[str] = Field(default=None, description="Tumor site")
    histology: Optional[str] = Field(default=None, description="Histology")
    primary_site: Optional[str] = Field(default=None, description="Primary site")
    primary_histology: Optional[str] = Field(default=None, description="Primary histology")
    mutation_description: Optional[str] = Field(default=None, description="Mutation description")

class DbNSFPPrediction(BaseModel):
    """dbNSFP functional predictions"""
    model_config = ConfigDict(extra='allow')
    
    sift_pred: Optional[str] = Field(default=None, description="SIFT prediction")
    polyphen2_hdiv_pred: Optional[str] = Field(default=None, description="PolyPhen2 HDIV prediction")
    polyphen2_hvar_pred: Optional[str] = Field(default=None, description="PolyPhen2 HVAR prediction")
    lrt_pred: Optional[str] = Field(default=None, description="LRT prediction")
    mutationtaster_pred: Optional[str] = Field(default=None, description="MutationTaster prediction")
    fathmm_pred: Optional[str] = Field(default=None, description="FATHMM prediction")
    metasvm_pred: Optional[str] = Field(default=None, description="MetaSVM prediction")
    metalr_pred: Optional[str] = Field(default=None, description="MetaLR prediction")

class DbSNPAllele(BaseModel):
    """dbSNP allele information"""
    allele: str = Field(description="Allele value")
    freq: Dict[str, float] = Field(description="Frequency information")

class DbSNPAnnotation(BaseModel):
    """dbSNP variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    rsid: Optional[str] = Field(default=None, description="dbSNP rs ID")
    dbsnp_build: Optional[int] = Field(default=None, description="dbSNP build")
    alleles: Optional[List[DbSNPAllele]] = Field(default=None, description="Observed alleles")
    allele_origin: Optional[str] = Field(default=None, description="Allele origin")
    validated: Optional[bool] = Field(default=None, description="Validation status")

class DoCMAnnotation(BaseModel):
    """DoCM variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    disease: Optional[str] = Field(default=None, description="Associated disease")
    domain: Optional[str] = Field(default=None, description="Protein domain")
    pathogenicity: Optional[str] = Field(default=None, description="Pathogenicity")
    pmid: Optional[List[str]] = Field(default=None, description="PubMed IDs")

class MutDBAnnotation(BaseModel):
    """MutDB variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    uniprot_id: Optional[str] = Field(default=None, description="UniProt ID")
    mutdb_id: Optional[str] = Field(default=None, description="MutDB ID")
    ref_aa: Optional[str] = Field(default=None, description="Reference amino acid")
    alt_aa: Optional[str] = Field(default=None, description="Alternative amino acid")
    position: Optional[int] = Field(default=None, description="Position in protein")

class SnpEffAnnotation(BaseModel):
    """SnpEff variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    ann: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = Field(default=None, description="Annotation details")
    effect: Optional[str] = Field(default=None, description="Variant effect")
    putative_impact: Optional[str] = Field(default=None, description="Putative impact")
    gene_name: Optional[str] = Field(default=None, description="Gene name")
    gene_id: Optional[str] = Field(default=None, description="Gene ID")
    feature_type: Optional[str] = Field(default=None, description="Feature type")
    transcript_biotype: Optional[str] = Field(default=None, description="Transcript biotype")

class VariantResponse(BaseModel):
    """Response model for variant information"""
    model_config = ConfigDict(extra='allow')
    
    id: str = Field(description="Variant identifier", validation_alias="_id")
    version: int = Field(description="Version number", validation_alias="_version")
    chrom: str = Field(description="Chromosome number")
    hg19: GenomicLocation = Field(description="HG19 genomic location")
    vcf: VCFInfo = Field(description="VCF information")
    
    # Typed optional annotation fields
    cadd: Optional[CADDScore] = Field(default=None, description="CADD scores and predictions")
    clinvar: Optional[ClinVarAnnotation] = Field(default=None, description="ClinVar annotations")
    cosmic: Optional[CosmicAnnotation] = Field(default=None, description="COSMIC annotations")
    dbnsfp: Optional[DbNSFPPrediction] = Field(default=None, description="dbNSFP functional predictions")
    dbsnp: Optional[DbSNPAnnotation] = Field(default=None, description="dbSNP annotations")
    docm: Optional[DoCMAnnotation] = Field(default=None, description="DoCM annotations")
    mutdb: Optional[MutDBAnnotation] = Field(default=None, description="MutDB annotations")
    snpeff: Optional[SnpEffAnnotation] = Field(default=None, description="SnpEff annotations")

    def get_variant_id(self) -> str:
        """Get the variant identifier in a standardized format"""
        return f"{self.chrom}:g.{self.vcf.position}{self.vcf.ref}>{self.vcf.alt}"

    def has_clinical_significance(self) -> bool:
        """Check if the variant has clinical significance information"""
        return self.clinvar is not None

    def has_functional_predictions(self) -> bool:
        """Check if the variant has functional predictions"""
        return any([
            self.cadd is not None,
            self.dbnsfp is not None,
            self.snpeff is not None
        ])

class VariantClient(AbstractClient[VariantResponse]):
    """A typed wrapper around the BioThings variant client (synchronous)"""
    
    def __init__(self):
        super().__init__("variant")
        
    def _response_model(self) -> type[VariantResponse]:
        return VariantResponse

    def getvariant(
        self,
        variant_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[VariantResponse]:
        """
        Get variant information by ID
        
        Args:
            variant_id: The variant identifier (e.g. "chr7:g.140453134T>C")
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            VariantResponse object containing the variant information or None if not found
        """
        result = self._client.getvariant(variant_id, fields=fields, **kwargs)
        if result is None:
            return None
        return VariantResponse.model_validate(result)
        
    def getvariants(
        self,
        variant_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[VariantResponse]:
        """
        Get information for multiple variants
        
        Args:
            variant_ids: List of variant identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of VariantResponse objects
        """
        if isinstance(variant_ids, str):
            variant_ids = variant_ids.split(",")
        elif isinstance(variant_ids, tuple):
            variant_ids = list(variant_ids)
            
        results = self._client.getvariants(variant_ids, fields=fields, **kwargs)
        return [VariantResponse.model_validate(result) for result in results]

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
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        """
        Query variants
        
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
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Query for many variants
        
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
        Get metadata about the variant database
        
        Returns:
            Dictionary containing database metadata
        """
        return self._client.metadata()

class VariantClientAsync(AbstractClientAsync[VariantResponse]):
    """A typed wrapper around the BioThings variant client (asynchronous)"""
    
    def __init__(self):
        super().__init__("variant")
        
    def _response_model(self) -> type[VariantResponse]:
        return VariantResponse

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
            
    async def getvariant(
        self,
        variant_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[VariantResponse]:
        """
        Get variant information by ID
        
        Args:
            variant_id: The variant identifier (e.g. "chr7:g.140453134T>C")
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            VariantResponse object containing the variant information or None if not found
        """
        result = await self._client.getvariant(variant_id, fields=fields, **kwargs)
        if result is None:
            return None
        return VariantResponse.model_validate(result)
        
    async def getvariants(
        self,
        variant_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[VariantResponse]:
        """
        Get information for multiple variants
        
        Args:
            variant_ids: List of variant identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of VariantResponse objects
        """
        if isinstance(variant_ids, str):
            variant_ids = variant_ids.split(",")
        elif isinstance(variant_ids, tuple):
            variant_ids = list(variant_ids)
            
        results = await self._client.getvariants(variant_ids, fields=fields, **kwargs)
        return [VariantResponse.model_validate(result) for result in results]

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
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        """
        Query variants
        
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
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """
        Query for many variants
        
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
        Get metadata about the variant database
        
        Returns:
            Dictionary containing database metadata
        """
        return await self._client.metadata()

if __name__ == "__main__":
    # Example usage for sync client
    client = VariantClient()
    variant = client.getvariant("chr7:g.140453134T>C")
    if variant:
        print(f"Variant ID: {variant.get_variant_id()}")
        print(f"Has clinical significance: {variant.has_clinical_significance()}")
        print(f"Has functional predictions: {variant.has_functional_predictions()}")
        print("\nFull variant data:")
        print(variant.model_dump_json(indent=2))
    
    # Example usage for async client
    import asyncio
    
    async def main():
        client = VariantClientAsync()
        variant = await client.getvariant("chr7:g.140453134T>C")
        if variant:
            print(f"Variant ID: {variant.get_variant_id()}")
            print(f"Has clinical significance: {variant.has_clinical_significance()}")
            print(f"Has functional predictions: {variant.has_functional_predictions()}")
            print("\nFull variant data:")
            print(variant.model_dump_json(indent=2))
        
        # Example query
        results = await client.query("dbnsfp.genename:cdk2", size=5)
        print("\nQuery results:")
        print(results)
        
    asyncio.run(main())