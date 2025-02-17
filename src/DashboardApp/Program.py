from waitress import serve

from dash import  Dash
import dash_bootstrap_components as dbc
from dash_auth import BasicAuth

import os
import sys
import dash
import configparser

from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.api_client import ApiClient
from DashboardAgrotechApp.const import Constant

class Program():
    """
    Main application program class for the Agrotech Dashboard.

    This class initializes the required components, such as the logger, API client, constants, and dashboard layout.
    It also sets up and runs the Dash application server.

    Attributes:
    -----------
        config (ConfigParser): 
            Instance of `configparser.ConfigParser` for loading and managing configuration settings.
        logger (Logger): 
            Instance of the Logger class for logging events.
        agrotech_api (ApiClient): 
            Instance of the ApiClient class for API interactions.
        constants (Constant): 
            Instance of the Constant class for storing and managing constant data.
        app (Dash): 
            The Dash application instance.
    """
    def __init__(self):
        """
        Initializes the Program class.

        This method sets up:
        - The logger for logging application events.
        - The API client for interacting with the Agrotech API.
        - Constants for application-wide values.
        - Configuration from a `config.ini` file.

        Attributes:
        -----------
        config (ConfigParser): 
            Parses and loads configuration from `config.ini`.

        Raises:
        -------
        FileNotFoundError: 
            If the `config.ini` file is not found or inaccessible.
        """
        self.config = configparser.ConfigParser()
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        
        self.logger =Logger()
        self.config.read(os.path.join(base_path,'config.ini'))
        self.agrotech_api = ApiClient()
        self.agrotech_api.login()
        self.constants = Constant(self.agrotech_api)

    def authorization_function(self,user_name:str, password:str):
        """
        Validates the user's credentials for accessing the dashboard.

        Args:
        -----
        user_name (str): 
            The username provided by the user.
        password (str): 
            The password provided by the user.

        Returns:
        --------
        bool: 
            True if the credentials are valid, False otherwise.
        """
        if (user_name == self.config['API']['user_name']) and (password == self.config['API']['password']):
            return True
        return False        

    def run(self):
        """
        Runs the Dash application server in debug mode.
        """
        app.run_server(debug=True)

    def main(self):
        """
        Provides access to the underlying WSGI server instance of the Dash application.

        Returns:
        --------
            Flask: The Flask server instance used by the Dash application.
        """
        app = Dash(__name__, 
            use_pages = True,
            assets_folder= "./assets",
            external_stylesheets=[dbc.themes.BOOTSTRAP])
        app._favicon = 'icon.ico'
        app.server.secret_key = self.config['API']['secret_key']
        BasicAuth(app, auth_func = self.authorization_function)
        return app.server      

if __name__ == "__main__":
    program = Program()
    app = program.main()        
    serve(app,host='0.0.0.0', port=8050)
    