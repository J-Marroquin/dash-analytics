from .api_client import ApiClient
import pandas as pd

class Constant:
    """
    A utility class to manage and provide constant data, such as warehouse information, retrieved from an external API.

    Attributes:
    -----------
    api_client (ApiClient): 
        An instance of the ApiClient class to interact with the API.
    _warehouses_data (pd.DataFrame): 
        A DataFrame containing warehouse data fetched from the API.
    """
    def __init__(self, api_client:ApiClient):
        """
        Initializes the Constant class by fetching warehouse data from the API.

        Args:
        -----
        api_client (ApiClient): 
            An instance of the ApiClient class to interact with the API.
        """
        self.api_client = api_client
        self._warehouses_data = self.api_client.execute_query("Query30", "OWHS")
    
    @property
    def warehouses_data(self)->pd.DataFrame:
        """
        Provides access to the warehouse data.

        Returns:
        --------
        pd.DataFrame:
            A DataFrame containing the warehouse data fetched from the API.
        """
        return self._warehouses_data