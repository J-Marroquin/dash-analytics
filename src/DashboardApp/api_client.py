import os
import sys
import requests
import configparser
import pandas as pd
from DashboardAgrotechApp.logger import Logger

class ApiClient():
    """
    A client class for interacting with an external API to execute queries and fetch data as pandas DataFrames.

    Attributes:
    -----------
        config (ConfigParser): 
            Configuration parser for reading the `config.ini` file.
        api (str): 
            Base URL of the API, fetched from the configuration file.
        _authorization (str): 
            Authorization token used for API requests.
        logger (Logger): 
            Logger instance for logging errors and information.
    """

    def __init__(self):
        """
        Initializes the ApiClient by loading configuration and setting up the API base URL.
        
        If the script is bundled (e.g., with PyInstaller), it handles the frozen state to find the correct config file path.
        """
        self.config=configparser.ConfigParser()
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        self.config.read(os.path.join(base_path,'config.ini'))
        self.api = self.config['API']['url']
        self._authorization = ""
        self.logger = Logger()

    @property
    def authorization(self)->str:
        """
        Lazy-loaded property that retrieves the authorization token.
        If the token is not already set, it triggers the login process.

        Returns:
        --------
            str: The authorization token.
        """
        if self._authorization == "":
            self.login()
        return self._authorization
        
    def login(self):
        """
        Authenticates the user by sending login credentials to the API.

        Reads the username and password from the configuration file, performs a POST request to the API's login endpoint,
        and retrieves the authorization token upon successful login.

        Logs an error if the login request fails.
        """
        login_body = {
            "UserName": self.config['API']['user_name'],
            "Password": self.config['API']['password']
        }
        login_post = requests.post(self.api + "login", json = login_body)
        if login_post.status_code == 200:
            _token = login_post.json().get("token")
            _authorization = {
            "Authorization": f"Bearer {_token}"
            }
            self._authorization = _authorization
        else:
            self.logger.log_error(f"Error during login. Please check the server status. StatusCode: {login_post.status_code}")
    
    def execute_query(self, sqlCode:str ,table_name:str, params:str="")-> pd.DataFrame:
        """
        Executes a SQL query by sending a GET request to the API and returns the result as a pandas DataFrame.

        Args:
        -----
            sqlCode (str): 
                The SQL code or identifier for the query.
            table_name (str): 
                The name of the table to fetch data from.
            params (str, optional): 
                Additional query parameters for pagination or filtering. Defaults to an empty string.

        Returns:
        --------
            pd.DataFrame: 
                A pandas DataFrame containing the query result.
            None: 
                If an error occurs during the GET request or data processing.
        """
        url_get = self.api + f"execquery?sqlcode={sqlCode}" + params 
        print(url_get)
        response_get = requests.get(url_get,headers = self.authorization)
        if response_get.status_code == 200:
            df = self.json_to_dataframe(response_get.json(),table_name)
            return df
        elif response_get.status_code == 204:
            return pd.DataFrame()
        else:
            self.logger.log_error(f"Error in GET request {url_get}. Status code: {response_get.status_code}")
            return None

    def json_to_dataframe(self,response_json:dict,table_name:str)->pd.DataFrame:
        """
        Converts a JSON response from the API into a pandas DataFrame.

        Args:
        -----
            response_json (dict): 
                The JSON response received from the API.
            table_name (str): 
                The name of the table to extract data from within the JSON structure.

        Returns:
        --------
            pd.DataFrame: A pandas DataFrame containing the extracted data.
            None: If an error occurs during the conversion process.
        """
        try:
            table_data = response_json.get("data", {}).get("BOM", {}).get("BO", {}).get(table_name, {}).get("row", [])
            df = pd.DataFrame(table_data)
            return df
        except Exception as ex:
            self.logger.log_error(f"Error converting dictionary to DataFrame: {ex}")
            return None

if __name__ == "__main__":
    api = ApiClient()
    api.login()
    df = api.execute_query('query32', table_name='OPDN', params= "&Pagesize=500&pagenumber=1")
    print(df)
    df.to_csv(r'C:\Users\jmarroquin\Downloads\compras.csv', index=False)

