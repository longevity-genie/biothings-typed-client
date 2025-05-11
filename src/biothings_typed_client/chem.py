from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd

from biothings_typed_client.abstract_client import AbstractClient, AbstractClientAsync

class PubChemInfo(BaseModel):
    """PubChem information for a chemical compound.
    
    This class represents detailed chemical information from PubChem, including structural properties,
    physical characteristics, and identifiers. The data is sourced from the PubChem database and
    provides comprehensive information about chemical compounds.
    
    Key fields include:
    - Structural information (SMILES, InChI, molecular formula)
    - Physical properties (molecular weight, exact mass)
    - Chemical properties (hydrogen bond donors/acceptors, rotatable bonds)
    - Stereochemistry information (chiral centers, stereocenters)
    - Chemical identifiers (CID, InChIKey)
    
    For more details on available fields and their meanings, see:
    https://docs.mychem.info/en/latest/doc/data.html#available-fields
    """
    model_config = ConfigDict(extra='allow')
    
    chiral_atom_count: Optional[int] = Field(default=None, description="Number of chiral atoms in the molecule")
    chiral_bond_count: Optional[int] = Field(default=None, description="Number of chiral bonds in the molecule")
    cid: Optional[Union[str, int]] = Field(default=None, description="PubChem Compound Identifier (CID)")
    complexity: Optional[float] = Field(default=None, description="Molecular complexity score (0-100)")
    covalently_bonded_unit_count: Optional[int] = Field(default=None, description="Number of covalently bonded units in the molecule")
    defined_atom_stereocenter_count: Optional[int] = Field(default=None, description="Number of defined atom stereocenters")
    defined_bond_stereocenter_count: Optional[int] = Field(default=None, description="Number of defined bond stereocenters")
    exact_mass: Optional[float] = Field(default=None, description="Exact molecular mass (monoisotopic mass)")
    formal_charge: Optional[int] = Field(default=None, description="Net formal charge of the molecule")
    heavy_atom_count: Optional[int] = Field(default=None, description="Number of non-hydrogen atoms")
    hydrogen_bond_acceptor_count: Optional[int] = Field(default=None, description="Number of hydrogen bond acceptor atoms")
    hydrogen_bond_donor_count: Optional[int] = Field(default=None, description="Number of hydrogen bond donor atoms")
    inchi: Optional[str] = Field(default=None, description="IUPAC International Chemical Identifier (InChI)")
    inchi_key: Optional[str] = Field(default=None, description="InChI Key (27-character hash of the InChI)")
    isotope_atom_count: Optional[int] = Field(default=None, description="Number of isotope atoms")
    iupac: Optional[Dict[str, str]] = Field(default=None, description="IUPAC names in different formats")
    molecular_formula: Optional[str] = Field(default=None, description="Molecular formula in Hill notation")
    molecular_weight: Optional[float] = Field(default=None, description="Average molecular weight")
    monoisotopic_weight: Optional[float] = Field(default=None, description="Monoisotopic molecular weight")
    rotatable_bond_count: Optional[int] = Field(default=None, description="Number of rotatable bonds")
    smiles: Optional[Dict[str, str]] = Field(default=None, description="SMILES strings in different formats")
    tautomers_count: Optional[int] = Field(default=None, description="Number of possible tautomers")
    topological_polar_surface_area: Optional[float] = Field(default=None, description="Topological polar surface area in Å²")
    undefined_atom_stereocenter_count: Optional[int] = Field(default=None, description="Number of undefined atom stereocenters")
    undefined_bond_stereocenter_count: Optional[int] = Field(default=None, description="Number of undefined bond stereocenters")
    xlogp: Optional[float] = Field(default=None, description="Octanol-water partition coefficient (logP)")

class ChemResponse(BaseModel):
    """Response model for chemical compound information from MyChem.info.
    
    This class represents the complete response from the MyChem.info API for a chemical compound.
    It includes the compound's identifier, version information, and detailed PubChem data.
    
    The response structure follows the MyChem.info API format and includes:
    - _id: The primary identifier (typically InChIKey)
    - _version: Version number of the data
    - pubchem: Detailed PubChem information (if available)
    
    For more information about the available fields and data sources, see:
    https://docs.mychem.info/en/latest/doc/data.html#available-fields
    """
    model_config = ConfigDict(extra='allow')
    
    id: str = Field(description="Chemical identifier (typically InChIKey)", validation_alias="_id")
    version: int = Field(default=1, description="Version number of the data", validation_alias="_version")
    pubchem: Optional[PubChemInfo] = Field(default=None, description="Detailed PubChem information")

    def get_chem_id(self) -> str:
        """Get the chemical identifier.
        
        Returns:
            str: The chemical identifier (typically InChIKey)
        """
        return self.id

    def has_pubchem(self) -> bool:
        """Check if the chemical has PubChem information.
        
        Returns:
            bool: True if PubChem information is available, False otherwise
        """
        return self.pubchem is not None

class ChemClient(AbstractClient[ChemResponse]):
    """A typed wrapper around the BioThings chem client (synchronous).
    
    This client provides synchronous access to the MyChem.info API, allowing you to retrieve
    chemical compound information using various identifiers. The client handles data caching
    and response parsing, providing strongly-typed responses through the ChemResponse model.
    
    The client supports:
    - Single compound lookup by ID
    - Batch compound lookup by multiple IDs
    - Field filtering to retrieve specific data
    - Response caching for improved performance
    
    For more information about the available fields and data sources, see:
    https://docs.mychem.info/en/latest/doc/data.html#available-fields
    """
    
    def __init__(self, caching: bool = True):
        """Initialize the chem client.
        
        Args:
            caching (bool): Whether to enable response caching. Defaults to True.
        """
        super().__init__("chem", caching=caching)
        
    def _response_model(self) -> type[ChemResponse]:
        """Get the response model type.
        
        Returns:
            type[ChemResponse]: The ChemResponse model class
        """
        return ChemResponse

    def getchem(
        self,
        chem_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[ChemResponse]:
        """Get chemical information by ID.
        
        This method retrieves detailed information about a single chemical compound
        using its identifier (typically an InChIKey). The response includes structural
        information, physical properties, and other chemical characteristics.
        
        Args:
            chem_id (str): The chemical identifier (e.g. InChI key)
            fields (Optional[Union[List[str], str]]): Specific fields to return. If None,
                all available fields are returned. Can be a single field name or a list
                of field names.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Optional[ChemResponse]: ChemResponse object containing the chemical information
                or None if not found
            
        Example:
            >>> client = ChemClient()
            >>> result = client.getchem("KTUFNOKKBVMGRW-UHFFFAOYSA-N")
            >>> print(result.pubchem.molecular_formula)
        """
        result = self._client.getchem(chem_id, fields=fields, **kwargs)
        if result is None:
            return None
        return ChemResponse.model_validate(result)
        
    def getchems(
        self,
        chem_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[ChemResponse]:
        """Get information for multiple chemicals.
        
        This method retrieves detailed information about multiple chemical compounds
        in a single request. It supports various input formats for the chemical IDs
        and allows field filtering to optimize response size.
        
        Args:
            chem_ids (Union[str, List[str], tuple]): List of chemical identifiers or
                comma-separated string. Can be:
                - A single string with comma-separated IDs
                - A list of ID strings
                - A tuple of ID strings
            fields (Optional[Union[List[str], str]]): Specific fields to return. If None,
                all available fields are returned. Can be a single field name or a list
                of field names.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List[ChemResponse]: List of ChemResponse objects containing the chemical
                information for each requested compound
            
        Example:
            >>> client = ChemClient()
            >>> results = client.getchems(["KTUFNOKKBVMGRW-UHFFFAOYSA-N", "XEFQLINVKFYRCS-UHFFFAOYSA-N"])
            >>> for result in results:
            ...     print(result.pubchem.molecular_formula)
        """
        if isinstance(chem_ids, str):
            chem_ids = chem_ids.split(",")
        elif isinstance(chem_ids, tuple):
            chem_ids = list(chem_ids)
            
        results = self._client.getchems(chem_ids, fields=fields, **kwargs)
        return [ChemResponse.model_validate(result) for result in results]

class ChemClientAsync(AbstractClientAsync[ChemResponse]):
    """A typed wrapper around the BioThings chem client (asynchronous).
    
    This client provides asynchronous access to the MyChem.info API, allowing you to retrieve
    chemical compound information using various identifiers. The client handles data caching
    and response parsing, providing strongly-typed responses through the ChemResponse model.
    
    The client supports:
    - Single compound lookup by ID
    - Batch compound lookup by multiple IDs
    - Field filtering to retrieve specific data
    - Response caching for improved performance
    
    For more information about the available fields and data sources, see:
    https://docs.mychem.info/en/latest/doc/data.html#available-fields
    """
    
    def __init__(self, caching: bool = True):
        """Initialize the async chem client.
        
        Args:
            caching (bool): Whether to enable response caching. Defaults to True.
        """
        super().__init__("chem", caching=caching)
        
    def _response_model(self) -> type[ChemResponse]:
        """Get the response model type.
        
        Returns:
            type[ChemResponse]: The ChemResponse model class
        """
        return ChemResponse

    async def getchem(
        self,
        chem_id: str,
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> Optional[ChemResponse]:
        """Get chemical information by ID asynchronously.
        
        This method retrieves detailed information about a single chemical compound
        using its identifier (typically an InChIKey). The response includes structural
        information, physical properties, and other chemical characteristics.
        
        Args:
            chem_id (str): The chemical identifier (e.g. InChI key)
            fields (Optional[Union[List[str], str]]): Specific fields to return. If None,
                all available fields are returned. Can be a single field name or a list
                of field names.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Optional[ChemResponse]: ChemResponse object containing the chemical information
                or None if not found
            
        Example:
            >>> client = ChemClientAsync()
            >>> result = await client.getchem("KTUFNOKKBVMGRW-UHFFFAOYSA-N")
            >>> print(result.pubchem.molecular_formula)
        """
        result = await self._client.getchem(chem_id, fields=fields, **kwargs)
        if result is None:
            return None
        return ChemResponse.model_validate(result)
        
    async def getchems(
        self,
        chem_ids: Union[str, List[str], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[ChemResponse]:
        """Get information for multiple chemicals asynchronously.
        
        This method retrieves detailed information about multiple chemical compounds
        in a single request. It supports various input formats for the chemical IDs
        and allows field filtering to optimize response size.
        
        Args:
            chem_ids (Union[str, List[str], tuple]): List of chemical identifiers or
                comma-separated string. Can be:
                - A single string with comma-separated IDs
                - A list of ID strings
                - A tuple of ID strings
            fields (Optional[Union[List[str], str]]): Specific fields to return. If None,
                all available fields are returned. Can be a single field name or a list
                of field names.
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List[ChemResponse]: List of ChemResponse objects containing the chemical
                information for each requested compound
            
        Example:
            >>> client = ChemClientAsync()
            >>> results = await client.getchems(["KTUFNOKKBVMGRW-UHFFFAOYSA-N", "XEFQLINVKFYRCS-UHFFFAOYSA-N"])
            >>> for result in results:
            ...     print(result.pubchem.molecular_formula)
        """
        if isinstance(chem_ids, str):
            chem_ids = chem_ids.split(",")
        elif isinstance(chem_ids, tuple):
            chem_ids = list(chem_ids)
            
        results = await self._client.getchems(chem_ids, fields=fields, **kwargs)
        return [ChemResponse.model_validate(result) for result in results]