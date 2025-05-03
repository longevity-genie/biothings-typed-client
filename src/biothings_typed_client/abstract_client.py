from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from pydantic import BaseModel
from biothings_client import get_client, get_async_client

T = TypeVar('T', bound=BaseModel)

class AbstractClient(Generic[T]):
    """Abstract base class for BioThings clients (synchronous)"""
    
    def __init__(self, api_name: str):
        self._client = get_client(api_name)
        
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
    ) -> Union[Dict[str, Any], 'pd.DataFrame']:
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
        Query for many items
        
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
        Get metadata about the database
        
        Returns:
            Dictionary containing database metadata
        """
        return self._client.metadata()

    def _response_model(self) -> type[T]:
        """Get the response model class for this client"""
        raise NotImplementedError("Subclasses must implement _response_model")

class AbstractClientAsync(Generic[T]):
    """Abstract base class for BioThings clients (asynchronous)"""
    
    def __init__(self, api_name: str):
        self._client = get_async_client(api_name)
        self._closed = False
        
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
    ) -> Union[Dict[str, Any], 'pd.DataFrame']:
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
        Query for many items
        
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
        Get metadata about the database
        
        Returns:
            Dictionary containing database metadata
        """
        return await self._client.metadata()

    def _response_model(self) -> type[T]:
        """Get the response model class for this client"""
        raise NotImplementedError("Subclasses must implement _response_model")
