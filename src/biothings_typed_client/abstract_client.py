from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel
from biothings_client import get_client, get_async_client
import pandas as pd

T = TypeVar('T', bound=BaseModel)

class AbstractClient(Generic[T]):
    """Abstract base class for BioThings clients (synchronous)"""
    
    def __init__(self, api_name: str, caching: bool = True):
        self._client = get_client(api_name)
        if caching:
            self.set_caching()
        
    def set_caching(self) -> None:
        """
        Enable caching for the client.
        This will cache responses from the API to improve performance.
        """
        self._client.set_caching()
        
    def stop_caching(self) -> None:
        """
        Disable caching for the client.
        This will stop caching responses from the API.
        """
        self._client.stop_caching()
        
    def clear_cache(self) -> None:
        """
        Clear the client's cache.
        This will remove all cached responses.
        """
        self._client.clear_cache()
        
    @property
    def caching_enabled(self) -> bool:
        """
        Check if caching is enabled for the client.
        
        Returns:
            bool: True if caching is enabled, False otherwise
        """
        return self._client.caching_enabled
        
    def get(self, id: Union[str, int], fields: Optional[Union[List[str], str]] = None, **kwargs) -> Optional[T]:
        """
        Get information by ID
        
        Args:
            id: The identifier
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Response object containing the information or None if not found
        """
        result = self._client.get(id, fields=fields, **kwargs)
        if result is None:
            return None
        return self._response_model().model_validate(result)
        
    def getmany(
        self,
        ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[T]:
        """
        Get information for multiple items
        
        Args:
            ids: List of identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of response objects
        """
        if isinstance(ids, str):
            ids = ids.split(",")
        elif isinstance(ids, tuple):
            ids = list(ids)
            
        results = self._client.getmany(ids, fields=fields, **kwargs)
        return [self._response_model().model_validate(result) for result in results]

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
        Query items
        
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
            Query results as a dictionary or pandas DataFrame. The dictionary will have the structure:
            {
                "hits": [
                    {
                        "_id": "identifier",
                        "_score": float,
                        # ... other fields ...
                    }
                ],
                "max_score": float,
                "took": int,
                "total": int
            }
            If no results are found, returns an empty dictionary with the same structure.
        """
        result = self._client.query(
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
        
        # Handle None result
        if result is None:
            return {
                "hits": [],
                "max_score": 0.0,
                "took": 0,
                "total": 0
            }
            
        # Ensure result has the expected structure
        if not isinstance(result, dict):
            return {
                "hits": [],
                "max_score": 0.0,
                "took": 0,
                "total": 0
            }
            
        if "hits" not in result:
            result["hits"] = []
            
        if "max_score" not in result:
            result["max_score"] = 0.0
            
        if "took" not in result:
            result["took"] = 0
            
        if "total" not in result:
            result["total"] = len(result.get("hits", []))
            
        return result

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
        Query multiple items
        
        Args:
            query_list: List of query strings or comma-separated string
            scopes: Fields to search in
            fields: Specific fields to return
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of query results or pandas DataFrame. Each result will have the structure:
            {
                "hits": [
                    {
                        "_id": "identifier",
                        "_score": float,
                        # ... other fields ...
                    }
                ],
                "max_score": float,
                "took": int,
                "total": int
            }
            If no results are found for a query, returns an empty dictionary with the same structure.
        """
        if isinstance(query_list, str):
            query_list = query_list.split(",")
        elif isinstance(query_list, tuple):
            query_list = list(query_list)
            
        results = self._client.querymany(
            query_list,
            scopes=scopes,
            fields=fields,
            species=species,
            email=email,
            **kwargs
        )
        
        # Handle None or invalid results
        if results is None:
            return []
            
        if not isinstance(results, list):
            return []
            
        # Ensure each result has the expected structure
        processed_results = []
        for result in results:
            if result is None:
                processed_results.append({
                    "hits": [],
                    "max_score": 0.0,
                    "took": 0,
                    "total": 0
                })
                continue
                
            if not isinstance(result, dict):
                processed_results.append({
                    "hits": [],
                    "max_score": 0.0,
                    "took": 0,
                    "total": 0
                })
                continue
                
            if "hits" not in result:
                result["hits"] = []
                
            if "max_score" not in result:
                result["max_score"] = 0.0
                
            if "took" not in result:
                result["took"] = 0
                
            if "total" not in result:
                result["total"] = len(result.get("hits", []))
                
            processed_results.append(result)
            
        return processed_results

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
        Get metadata about the database
        
        Returns:
            Dictionary containing database metadata
        """
        return self._client.metadata()

    def _response_model(self) -> type[T]:
        """Get the response model class for this client"""
        raise NotImplementedError("Subclasses must implement _response_model")

class AbstractClientAsync(Generic[T]):
    """Abstract base class for BioThings clients (asynchronous)
    
    For proper caching setup, use as an async context manager:
        async with ClientAsync() as client:
            result = await client.get("some_id")
    
    Or manually enable caching after instantiation:
        client = ClientAsync()
        await client.set_caching()
        result = await client.get("some_id")
    """
    
    def __init__(self, api_name: str, caching: bool = True):
        self._client = get_async_client(api_name)
        self._closed = False
        self._enable_caching = caching
    
    @classmethod
    async def create(cls, caching: bool = True):
        """
        Create and initialize an async client with caching properly set up.
        
        This is a convenience factory method for users who don't want to use
        the async context manager pattern.
        
        Args:
            caching: Whether to enable caching
            
        Returns:
            Fully initialized async client
            
        Example:
            client = await GeneClientAsync.create(caching=True)
            result = await client.get("some_id")
        """
        instance = cls(caching=False)  # Don't auto-enable caching
        if caching:
            await instance.set_caching()
        return instance
        
    async def __aenter__(self):
        if self._enable_caching:
            await self.set_caching()
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
            
    async def set_caching(self) -> None:
        """
        Enable caching for the client.
        This will cache responses from the API to improve performance.
        """
        await self._client.set_caching()
        
    async def stop_caching(self) -> None:
        """
        Disable caching for the client.
        This will stop caching responses from the API.
        """
        await self._client.stop_caching()
        
    async def clear_cache(self) -> None:
        """
        Clear the client's cache.
        This will remove all cached responses.
        """
        await self._client.clear_cache()
        
    @property
    def caching_enabled(self) -> bool:
        """
        Check if caching is enabled for the client.
        
        Returns:
            bool: True if caching is enabled, False otherwise
        """
        return self._client.caching_enabled
        
    async def get(self, id: Union[str, int], fields: Optional[Union[List[str], str]] = None, **kwargs) -> Optional[T]:
        """
        Get information by ID
        
        Args:
            id: The identifier
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            Response object containing the information or None if not found
        """
        result = await self._client.get(id, fields=fields, **kwargs)
        if result is None:
            return None
        return self._response_model().model_validate(result)
        
    async def getmany(
        self,
        ids: Union[str, List[Union[str, int]], tuple],
        fields: Optional[Union[List[str], str]] = None,
        **kwargs
    ) -> List[T]:
        """
        Get information for multiple items
        
        Args:
            ids: List of identifiers or comma-separated string
            fields: Specific fields to return
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of response objects
        """
        if isinstance(ids, str):
            ids = ids.split(",")
        elif isinstance(ids, tuple):
            ids = list(ids)
            
        results = await self._client.getmany(ids, fields=fields, **kwargs)
        return [self._response_model().model_validate(result) for result in results]

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
        Query items
        
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
            Query results as a dictionary or pandas DataFrame. The dictionary will have the structure:
            {
                "hits": [
                    {
                        "_id": "identifier",
                        "_score": float,
                        # ... other fields ...
                    }
                ],
                "max_score": float,
                "took": int,
                "total": int
            }
            If no results are found, returns an empty dictionary with the same structure.
        """
        result = await self._client.query(
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
        
        # Handle None result
        if result is None:
            return {
                "hits": [],
                "max_score": 0.0,
                "took": 0,
                "total": 0
            }
            
        # Ensure result has the expected structure
        if not isinstance(result, dict):
            return {
                "hits": [],
                "max_score": 0.0,
                "took": 0,
                "total": 0
            }
            
        if "hits" not in result:
            result["hits"] = []
            
        if "max_score" not in result:
            result["max_score"] = 0.0
            
        if "took" not in result:
            result["took"] = 0
            
        if "total" not in result:
            result["total"] = len(result.get("hits", []))
            
        return result

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
        Query multiple items
        
        Args:
            query_list: List of query strings or comma-separated string
            scopes: Fields to search in
            fields: Specific fields to return
            species: Species names or taxonomy ids
            email: User email for tracking usage
            as_dataframe: Return results as pandas DataFrame
            df_index: Index DataFrame by query (only if as_dataframe=True)
            **kwargs: Additional arguments passed to the underlying client
            
        Returns:
            List of query results or pandas DataFrame. Each result will have the structure:
            {
                "hits": [
                    {
                        "_id": "identifier",
                        "_score": float,
                        # ... other fields ...
                    }
                ],
                "max_score": float,
                "took": int,
                "total": int
            }
            If no results are found for a query, returns an empty dictionary with the same structure.
        """
        if isinstance(query_list, str):
            query_list = query_list.split(",")
        elif isinstance(query_list, tuple):
            query_list = list(query_list)
            
        results = await self._client.querymany(
            query_list,
            scopes=scopes,
            fields=fields,
            species=species,
            email=email,
            **kwargs
        )
        
        # Handle None or invalid results
        if results is None:
            return []
            
        if not isinstance(results, list):
            return []
            
        # Ensure each result has the expected structure
        processed_results = []
        for result in results:
            if result is None:
                processed_results.append({
                    "hits": [],
                    "max_score": 0.0,
                    "took": 0,
                    "total": 0
                })
                continue
                
            if not isinstance(result, dict):
                processed_results.append({
                    "hits": [],
                    "max_score": 0.0,
                    "took": 0,
                    "total": 0
                })
                continue
                
            if "hits" not in result:
                result["hits"] = []
                
            if "max_score" not in result:
                result["max_score"] = 0.0
                
            if "took" not in result:
                result["took"] = 0
                
            if "total" not in result:
                result["total"] = len(result.get("hits", []))
                
            processed_results.append(result)
            
        return processed_results

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
        Get metadata about the database
        
        Returns:
            Dictionary containing database metadata
        """
        return await self._client.metadata()

    def _response_model(self) -> type[T]:
        """Get the response model class for this client"""
        raise NotImplementedError("Subclasses must implement _response_model")
