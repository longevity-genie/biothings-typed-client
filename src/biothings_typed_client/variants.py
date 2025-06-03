from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd
from biothings_typed_client.abstract_client import AbstractClient, AbstractClientAsync

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
    
    # Additional fields from example
    alt: Optional[str] = Field(default=None, description="Alternative allele")
    anc: Optional[str] = Field(default=None, description="Ancestral allele")
    annotype: Optional[Union[str, List[str]]] = Field(default=None, description="Annotation type")
    bstatistic: Optional[float] = Field(default=None, description="B-statistic score")
    chmm: Optional[Dict[str, float]] = Field(default=None, description="Chromatin state predictions")
    chrom: Optional[Union[str, int]] = Field(default=None, description="Chromosome")
    conscore: Optional[float] = Field(default=None, description="Conservation score")
    cpg: Optional[float] = Field(default=None, description="CpG island score")
    dna: Optional[Dict[str, float]] = Field(default=None, description="DNA structure predictions")
    encode: Optional[Dict[str, Any]] = Field(default=None, description="ENCODE data")
    esp: Optional[Dict[str, float]] = Field(default=None, description="ESP allele frequencies")
    exon: Optional[str] = Field(default=None, description="Exon number")
    fitcons: Optional[float] = Field(default=None, description="FITCONS score")
    gc: Optional[float] = Field(default=None, description="GC content")
    gene: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(default=None, description="Gene information")
    gerp: Optional[Dict[str, float]] = Field(default=None, description="GERP scores")
    grantham: Optional[float] = Field(default=None, description="Grantham score")
    isderived: Optional[str] = Field(default=None, description="Is derived allele")
    isknownvariant: Optional[str] = Field(default=None, description="Is known variant")
    istv: Optional[str] = Field(default=None, description="Is TV")
    length: Optional[int] = Field(default=None, description="Variant length")
    mapability: Optional[Dict[str, int]] = Field(default=None, description="Mapability scores")
    min_dist_tse: Optional[int] = Field(default=None, description="Min distance to TSE")
    min_dist_tss: Optional[int] = Field(default=None, description="Min distance to TSS")
    mutindex: Optional[float] = Field(default=None, description="Mutation index")
    naa: Optional[str] = Field(default=None, description="New amino acid")
    oaa: Optional[str] = Field(default=None, description="Original amino acid")
    phast_cons: Optional[Dict[str, float]] = Field(default=None, description="PhastCons scores")
    phylop: Optional[Dict[str, float]] = Field(default=None, description="PhyloP scores")
    polyphen: Optional[Dict[str, Any]] = Field(default=None, description="PolyPhen predictions")
    pos: Optional[int] = Field(default=None, description="Position")
    rawscore: Optional[float] = Field(default=None, description="Raw score")
    ref: Optional[str] = Field(default=None, description="Reference allele")
    segway: Optional[str] = Field(default=None, description="Segway annotation")
    sift: Optional[Dict[str, Any]] = Field(default=None, description="SIFT predictions")
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
    
    # Additional fields from example
    license: Optional[str] = Field(default=None, description="License information")
    allele_id: Optional[int] = Field(default=None, description="Allele ID")
    alt: Optional[str] = Field(default=None, description="Alternative allele")
    chrom: Optional[str] = Field(default=None, description="Chromosome")
    cytogenic: Optional[str] = Field(default=None, description="Cytogenic location")
    gene: Optional[Dict[str, Any]] = Field(default=None, description="Gene information")
    hg19: Optional[GenomicLocation] = Field(default=None, description="HG19 genomic location")
    hg38: Optional[GenomicLocation] = Field(default=None, description="HG38 genomic location")
    hgvs: Optional[Dict[str, List[str]]] = Field(default=None, description="HGVS notations")
    rcv: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(default=None, description="RCV information")
    ref: Optional[str] = Field(default=None, description="Reference allele")
    rsid: Optional[str] = Field(default=None, description="dbSNP rs ID")
    type: Optional[str] = Field(default=None, description="Variant type")
    variant_id: Optional[int] = Field(default=None, description="Variant ID")

class CosmicAnnotation(BaseModel):
    """COSMIC variant annotations"""
    model_config = ConfigDict(extra='allow')
    
    cosmic_id: Optional[str] = Field(default=None, description="COSMIC variant ID")
    tumor_site: Optional[str] = Field(default=None, description="Tumor site")
    histology: Optional[str] = Field(default=None, description="Histology")
    primary_site: Optional[str] = Field(default=None, description="Primary site")
    primary_histology: Optional[str] = Field(default=None, description="Primary histology")
    mutation_description: Optional[str] = Field(default=None, description="Mutation description")
    
    # Additional fields from example
    license: Optional[str] = Field(default=None, description="License information")
    alt: Optional[str] = Field(default=None, description="Alternative allele")
    chrom: Optional[str] = Field(default=None, description="Chromosome")
    hg19: Optional[GenomicLocation] = Field(default=None, description="HG19 genomic location")
    mut_freq: Optional[float] = Field(default=None, description="Mutation frequency")
    mut_nt: Optional[str] = Field(default=None, description="Mutation nucleotide change")
    ref: Optional[str] = Field(default=None, description="Reference allele")

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
    version: int = Field(default=1, description="Version number", validation_alias="_version")
    chrom: str = Field(description="Chromosome number")
    hg19: Optional[GenomicLocation] = Field(default=None, description="HG19 genomic location")
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
    """
    A typed wrapper around the BioThings variant client (synchronous).
    
    This client provides methods to query and retrieve variant information from the MyVariant.info API.
    It supports various operations including getting single variants, batch queries, and field-specific searches.
    
    Example:
        ```python
        from biothings_typed_client.variants import VariantClient
        
        # Initialize the client
        client = VariantClient()
        
        # Get a single variant
        variant = client.getvariant("chr7:g.140453134T>C")
        if variant:
            print(f"Variant ID: {variant.get_variant_id()}")
            print(f"Has clinical significance: {variant.has_clinical_significance()}")
            
        # Query variants using different syntax
        # Simple queries
        results = client.query("rs58991260")
        results = client.query("chr1:69000-70000")
        
        # Fielded queries
        results = client.query("dbsnp.vartype:snp")
        results = client.query("dbnsfp.polyphen2.hdiv.pred:(D P)")
        results = client.query("dbnsfp.polyphen2.hdiv.pred:(D OR P)")
        results = client.query("_exists_:dbsnp")
        results = client.query("_missing_:exac")
        
        # Range queries
        results = client.query("dbnsfp.polyphen2.hdiv.score:>0.99")
        results = client.query("dbnsfp.polyphen2.hdiv.score:>=0.99")
        results = client.query("exac.af:<0.00001")
        results = client.query("exac.af:<=0.00001")
        results = client.query("exac.ac.ac_adj:[76640 TO 80000]")
        results = client.query("exac.ac.ac_adj:{76640 TO 80000}")
        
        # Wildcard queries
        results = client.query("dbnsfp.genename:CDK?")
        results = client.query("dbnsfp.genename:CDK*")
        
        # Boolean operators
        results = client.query("_exists_:dbsnp AND dbsnp.vartype:snp")
        results = client.query("dbsnp.vartype:snp OR dbsnp.vartype:indel")
        results = client.query("_exists_:dbsnp AND NOT dbsnp.vartype:indel")
        results = client.query("_exists_:dbsnp AND (NOT dbsnp.vartype:indel)")
        ```
    """
    
    def __init__(self, caching: bool = True):
        """
        Initialize the variant client.
        
        Args:
            caching: Whether to enable response caching. Defaults to True.
                    When enabled, responses are cached to improve performance for repeated queries.
        """
        super().__init__("variant", caching=caching)
        
    def _response_model(self) -> type[VariantResponse]:
        """
        Get the response model class for this client.
        
        Returns:
            The VariantResponse class used for parsing API responses
        """
        return VariantResponse

    def getvariant(
        self,
        variant_id: str,
        fields: Optional[Union[List[str], str]] = "all",
        **kwargs
    ) -> Optional[VariantResponse]:
        """
        Get variant information by ID.
        
        This method retrieves detailed information about a specific variant using its identifier.
        The variant ID can be in various formats including HGVS notation, rsID, or genomic coordinates.
        
        Args:
            variant_id: The variant identifier (e.g. "chr7:g.140453134T>C", "rs58991260")
            fields: Specific fields to return. Can be:
                   - "all" (default): Return all available fields
                   - A list of field names: Return only specified fields
                   - A comma-separated string: Return only specified fields
            **kwargs: Additional arguments passed to the underlying client:
                     - size: Maximum number of results to return
                     - from_: Starting position for pagination
                     - sort: Fields to sort by
                     - facets: Fields to compute facets for
                     
        Returns:
            VariantResponse object containing the variant information or None if not found
            
        Example:
            ```python
            # Get a variant with all fields
            variant = client.getvariant("chr7:g.140453134T>C")
            
            # Get specific fields only
            variant = client.getvariant("rs58991260", fields=["cadd.phred", "dbsnp.rsid"])
            ```
        """
        result = self._client.getvariant(variant_id, fields=fields, **kwargs)
        if result is None:
            return None
        return VariantResponse.model_validate(result)
        
    def getvariants(
        self,
        variant_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = "all",
        **kwargs
    ) -> List[VariantResponse]:
        """
        Get information for multiple variants in a single request.
        
        This method efficiently retrieves information for multiple variants in a single API call.
        It supports various input formats and can handle large numbers of variants.
        
        Args:
            variant_ids: List of variant identifiers or comma-separated string.
                        Can include HGVS notations, rsIDs, or genomic coordinates.
            fields: Specific fields to return. Can be:
                   - "all" (default): Return all available fields
                   - A list of field names: Return only specified fields
                   - A comma-separated string: Return only specified fields
            **kwargs: Additional arguments passed to the underlying client:
                     - size: Maximum number of results to return
                     - from_: Starting position for pagination
                     - sort: Fields to sort by
                     - facets: Fields to compute facets for
                     
        Returns:
            List of VariantResponse objects, one for each variant found
            
        Example:
            ```python
            # Get multiple variants using a list
            variants = client.getvariants(["chr7:g.140453134T>C", "rs58991260"])
            
            # Get multiple variants using a comma-separated string
            variants = client.getvariants("chr7:g.140453134T>C,rs58991260")
            
            # Get specific fields for multiple variants
            variants = client.getvariants(
                ["chr7:g.140453134T>C", "rs58991260"],
                fields=["cadd.phred", "dbsnp.rsid"]
            )
            ```
        """
        if isinstance(variant_ids, str):
            variant_ids = variant_ids.split(",")
        elif isinstance(variant_ids, tuple):
            variant_ids = list(variant_ids)
            
        results = self._client.getvariants(variant_ids, fields=fields, **kwargs)
        return [VariantResponse.model_validate(result) for result in results]

class VariantClientAsync(AbstractClientAsync[VariantResponse]):
    """
    An asynchronous typed wrapper around the BioThings variant client.
    
    This client provides the same functionality as VariantClient but with async/await support.
    It's particularly useful for applications that need to make multiple concurrent API calls
    or integrate with async frameworks.
    
    Example:
        ```python
        import asyncio
        from biothings_typed_client.variants import VariantClientAsync
        
        async def main():
            client = VariantClientAsync()
            
            # Get a single variant
            variant = await client.getvariant("chr7:g.140453134T>C")
            if variant:
                print(f"Variant ID: {variant.get_variant_id()}")
                
            # Query variants using different syntax
            # Simple queries
            results = await client.query("rs58991260")
            results = await client.query("chr1:69000-70000")
            
            # Fielded queries
            results = await client.query("dbsnp.vartype:snp")
            results = await client.query("dbnsfp.polyphen2.hdiv.pred:(D P)")
            results = await client.query("dbnsfp.polyphen2.hdiv.pred:(D OR P)")
            results = await client.query("_exists_:dbsnp")
            results = await client.query("_missing_:exac")
            
            # Range queries
            results = await client.query("dbnsfp.polyphen2.hdiv.score:>0.99")
            results = await client.query("dbnsfp.polyphen2.hdiv.score:>=0.99")
            results = await client.query("exac.af:<0.00001")
            results = await client.query("exac.af:<=0.00001")
            results = await client.query("exac.ac.ac_adj:[76640 TO 80000]")
            results = await client.query("exac.ac.ac_adj:{76640 TO 80000}")
            
            # Wildcard queries
            results = await client.query("dbnsfp.genename:CDK?")
            results = await client.query("dbnsfp.genename:CDK*")
            
            # Boolean operators
            results = await client.query("_exists_:dbsnp AND dbsnp.vartype:snp")
            results = await client.query("dbsnp.vartype:snp OR dbsnp.vartype:indel")
            results = await client.query("_exists_:dbsnp AND NOT dbsnp.vartype:indel")
            results = await client.query("_exists_:dbsnp AND (NOT dbsnp.vartype:indel)")
            
            await client.close()
            
        asyncio.run(main())
        ```
    """
    
    def __init__(self, caching: bool = True):
        """
        Initialize the async variant client.
        
        Args:
            caching: Whether to enable response caching. Defaults to True.
                    When enabled, responses are cached to improve performance for repeated queries.
        """
        super().__init__("variant", caching=caching)
        
    def _response_model(self) -> type[VariantResponse]:
        """
        Get the response model class for this client.
        
        Returns:
            The VariantResponse class used for parsing API responses
        """
        return VariantResponse

    async def __aenter__(self):
        """
        Enter the async context manager.
        
        Returns:
            The client instance
        """
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the async context manager.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        """
        await self.close()
            
    async def close(self):
        """
        Close the client connection and cleanup resources.
        
        This method should be called when the client is no longer needed to properly
        cleanup resources and close any open connections.
        """
        if not self._closed and hasattr(self._client, 'close'):
            try:
                await self._client.close()
            except Exception:
                # Ignore any errors during cleanup
                pass
            finally:
                self._closed = True
                
    def __del__(self):
        """
        Cleanup when the object is deleted.
        
        This method ensures that resources are properly cleaned up even if the client
        is not explicitly closed. However, to avoid "coroutine was never awaited" warnings,
        async resource cleanup is not performed during garbage collection.
        """
        if not self._closed:
            # Mark as closed to prevent further cleanup attempts
            self._closed = True
            
            # Don't try to close async resources during garbage collection
            # This can cause "coroutine was never awaited" warnings
            # Proper cleanup should be done via explicit close() calls or context managers
            
    async def getvariant(
        self,
        variant_id: str,
        fields: Optional[Union[List[str], str]] = "all",
        **kwargs
    ) -> Optional[VariantResponse]:
        """
        Asynchronously get variant information by ID.
        
        This method retrieves detailed information about a specific variant using its identifier.
        The variant ID can be in various formats including HGVS notation, rsID, or genomic coordinates.
        
        Args:
            variant_id: The variant identifier (e.g. "chr7:g.140453134T>C", "rs58991260")
            fields: Specific fields to return. Can be:
                   - "all" (default): Return all available fields
                   - A list of field names: Return only specified fields
                   - A comma-separated string: Return only specified fields
            **kwargs: Additional arguments passed to the underlying client:
                     - size: Maximum number of results to return
                     - from_: Starting position for pagination
                     - sort: Fields to sort by
                     - facets: Fields to compute facets for
                     
        Returns:
            VariantResponse object containing the variant information or None if not found
            
        Example:
            ```python
            # Get a variant with all fields
            variant = await client.getvariant("chr7:g.140453134T>C")
            
            # Get specific fields only
            variant = await client.getvariant("rs58991260", fields=["cadd.phred", "dbsnp.rsid"])
            ```
        """
        result = await self._client.getvariant(variant_id, fields=fields, **kwargs)
        if result is None:
            return None
        return VariantResponse.model_validate(result)
        
    async def getvariants(
        self,
        variant_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = "all",
        **kwargs
    ) -> List[VariantResponse]:
        """
        Asynchronously get information for multiple variants in a single request.
        
        This method efficiently retrieves information for multiple variants in a single API call.
        It supports various input formats and can handle large numbers of variants.
        
        Args:
            variant_ids: List of variant identifiers or comma-separated string.
                        Can include HGVS notations, rsIDs, or genomic coordinates.
            fields: Specific fields to return. Can be:
                   - "all" (default): Return all available fields
                   - A list of field names: Return only specified fields
                   - A comma-separated string: Return only specified fields
            **kwargs: Additional arguments passed to the underlying client:
                     - size: Maximum number of results to return
                     - from_: Starting position for pagination
                     - sort: Fields to sort by
                     - facets: Fields to compute facets for
                     
        Returns:
            List of VariantResponse objects, one for each variant found
            
        Example:
            ```python
            # Get multiple variants using a list
            variants = await client.getvariants(["chr7:g.140453134T>C", "rs58991260"])
            
            # Get multiple variants using a comma-separated string
            variants = await client.getvariants("chr7:g.140453134T>C,rs58991260")
            
            # Get specific fields for multiple variants
            variants = await client.getvariants(
                ["chr7:g.140453134T>C", "rs58991260"],
                fields=["cadd.phred", "dbsnp.rsid"]
            )
            ```
        """
        if isinstance(variant_ids, str):
            variant_ids = variant_ids.split(",")
        elif isinstance(variant_ids, tuple):
            variant_ids = list(variant_ids)
            
        results = await self._client.getvariants(variant_ids, fields=fields, **kwargs)
        return [VariantResponse.model_validate(result) for result in results]