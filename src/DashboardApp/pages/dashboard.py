from dash import  Dash, dash, dcc, html, Input, Output , State, callback_context, callback, register_page
from dash.exceptions import PageError
import dash_bootstrap_components as dbc
import dash_ag_grid as dag


import os
import sys
import configparser
import traceback
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from PIL import Image

from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.graph_manager import GraphManager
from DashboardAgrotechApp.api_client import ApiClient
from DashboardAgrotechApp.const import Constant
from DashboardAgrotechApp.layout.filters import filters_card

class Dashboard:
    """
    A class for managing and rendering the Agrotech Dashboard application using Dash.

    This class initializes the necessary components such as API client, constants, logger,
    and graph manager. It sets up the dashboard layout, loads configurations, fetches data
    from the API, and handles user interactions via callbacks.

    Attributes:
    -----------
    logger (Logger): 
        An instance of the Logger class for logging events.
    graph_manager (GraphManager): 
        Manages the functions used to render graphs.
    agrotech_api (ApiClient): 
        API client to interact with the Agrotech backend.
    const (Constant): 
        Provides constant data, such as warehouse information.
    graph_configs (dict): 
        Stores configuration for each graph defined in `config.ini`.
    graph_results (dict): 
        Caches the results of rendered graphs.
    data_results (dict): 
        Stores the data fetched for each graph.
    """
    def __init__(self,constant: Constant):
        """
        Initializes the Dashboard class by setting up necessary components and configurations.

        Args:
        -----
        constant (Constant): 
            An instance of the Constant class for managing constant data.
        """
        self.logger =Logger()
        self.graph_manager = GraphManager()
        self.agrotech_api = ApiClient()
        self.const = constant
        self.agrotech_api.login()
        self.graph_configs = {}
        self.graph_results = {}
        self.data_results ={}
        self.set_up()

    @property
    def season(self):
        """
        Determines the current season based on today's date.

        Returns:
        --------
            str: A string representing the season in the format "YYYY/YYYY".
        """
        today = dt.today()
        current_year = today.year
        next_year = current_year + 1
        last_year = current_year - 1

        if today < dt(today.year,11,1):
            last_year = current_year - 1
            _season = f'{last_year}/{current_year}'
        else:
            next_year = current_year + 1
            _season = f'{current_year}/{next_year}'
                        
        return _season

    def start(self):
        """
        Initializes and configures the Dash application layout and callbacks.

        Returns:
        --------
        Dash: 
            The Dash application instance.
        """
        filters_component, quick_ranges = filters_card()
        # Define el layout
        layout = html.Div(
            children=[
                dcc.Location(id="url"),
                dcc.Loading(
                    id="loading-overlay",
                    type="circle",
                    fullscreen=True,
                    children=[
                        dbc.Container(
                            fluid=True,
                            class_name= "px-0",
                            children=[
                                # Encabezado
                                dbc.Navbar(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://44e62736-28ca-4ccb-982c-f5151e678df0.avestruz.mx/logo.svg",  # Ruta relativa al directorio 'assets'
                                                        style={
                                                            "height": "50px",  # Tamaño en PC
                                                            "maxHeight": "10vh",  # Ajuste en móvil
                                                        },
                                                        className="d-none d-md-block"  # Oculta el logo en móvil
                                                    ),
                                                    width="auto",
                                                ),
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://44e62736-28ca-4ccb-982c-f5151e678df0.avestruz.mx/logo.svg",
                                                        style = {
                                                            "height": "clamp(6px, 15px, 30px)",  # Más pequeño en móvil
                                                            "maxHeight": "6vh",
                                                            "maxWidth": "30vw",
                                                            "display": "block",
                                                        },
                                                        className="d-md-none"  # Logo más pequeño en móvil
                                                    ),
                                                    width="auto",
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.NavbarBrand(
                                                            "Agrotech App",
                                                            style={
                                                                "fontSize": "clamp(1.2rem, 4vw, 3rem)",  #Se adapta a la pantalla
                                                                "color": "white",  # Texto en blanco
                                                                "fontWeight": "bold", 
                                                                "maxWidth": "60vw",  # Limita el ancho
                                                                "whiteSpace": "nowrap",  # Evita saltos de línea
                                                                "overflow": "hidden",
                                                                "marginLeft": "5px",  # Espaciado entre logo y texto
                                                            },
                                                        ),
                                                        html.P(
                                                        "Lo más relevante de la temporada 2024/2025",
                                                        style={
                                                            "fontSize": "clamp(0.9rem, 1.5vw, 2rem)",
                                                            "color": "white",
                                                            "marginTop": "-5px",  # Ajusta la posición vertical
                                                            "whiteSpace": "nowrap",
                                                            "overflow": "hidden",                                                            
                                                        },
                                                        )
                                                    ],
                                                    className="text-center",
                                                    width="auto",
                                                )
                                            ],
                                            align="center",  # Centra verticalmente
                                            className="g-0 d-flex justify-content-between",  # Ajuste horizontal
                                        ),
                                    ],
                                    color="#7A9F41",  # Fondo claro
                                    dark=True,  # Texto en blanco por defecto
                                    style={
                                        "top": 0,  # Parte superior
                                        "width": "100%",  # Ocupa todo el ancho
                                        "padding": "5px 10px",  # Ajusta el padding de los lados
                                        "height": "auto",
                                        "minHeight": "60px"
                                    },
                                ),
                            ]
                        ),
                        dbc.Container(
                            fluid=True,
                            children=[
                                # Filtros
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            # Contenedor de filtros
                                            filters_component,
                                            width=12,
                                            className="d-flex justify-content-center mb-4 mt-5"
                                        )
                                    ],
                                ),
                                # Tarjetas principales
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H5("HUEVOS REGISTRADOS", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(id="season-eggs-total", className="egg-stats"),
                                                                dbc.Col(id="last30-days-total", className="egg-stats"),
                                                                dbc.Col(id="month-eggs-total", className="egg-stats"),
                                                                dbc.Col(id="before-yesterday-eggs-total", className="egg-stats"),
                                                                dbc.Col(id="yesterday-eggs-total", className="egg-stats"),
                                                                dbc.Col(id="forecast-eggs", className="egg-stats"),
                                                            ],
                                                            className="text-center",
                                                        ),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                    },
                                            ),
                                            width=12,
                                        ),
                                    ],
                                    className="mb-4",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H5("POLLOS REGISTRADOS", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(id="season-chicks-total", className="egg-stats"),
                                                                dbc.Col(id="last30-days-total-chicks", className="egg-stats"),
                                                                dbc.Col(id="month-chicks-total", className="egg-stats"),
                                                                dbc.Col(id="before-yesterday-chicks-total", className="egg-stats"),
                                                                dbc.Col(id="yesterday-chicks-total", className="egg-stats"),
                                                                dbc.Col(id="forecast-chicks", className="egg-stats"),
                                                            ],
                                                            className="text-center",
                                                        ),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                    },
                                            ),
                                            width=12,
                                        ),
                                    ],
                                    className="mb-4",
                                ),
                                # Gráficos de consumo y gasto
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H5("MONTO REVALORIZADO POR ETAPA", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="material-revaluation-bar", 
                                                                config={"responsive": True},
                                                                style={"height": "350px"},
                                                                className="dash-graph-container"),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "width": "100%",
                                                    "height": "100%",
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                }
                                            ),
                                            width={"size": 12, "md": 6}, # 12 en móvil (una fila), 6 en pantallas medianas
                                            className="col-md-6 col-sm-12 mb-4",  # Se adapta a móvil
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H6("GASTO MENSUAL EN COMPRAS DE ALIMENTO", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="purchase-line-chart", 
                                                                config={"responsive": True}, 
                                                                style={"height": "350px", "width":"100%"},
                                                                className="dash-graph-container"),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        },                                                  
                                                    ),
                                                ],
                                                #className="shadow-sm",
                                                style={
                                                    "width": "100%",
                                                    "height": "100%",
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                }
                                            ),
                                            width={"size": 12, "md": 6},
                                            className="col-md-6 col-sm-12 mb-4",  # Se adapta a móvil
                                        ),
                                    ],
                                    className="mb-4"
                                ),
                                # Gráfico de registro de huevos
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H6("HISTÓRICO DEL REGISTRO DE HUEVOS", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="egg-registration-weekly", config={"responsive": True},style={"height": "100%"}, className="h-100"),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "height": "50vh",
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        }, 
                                                    ),
                                                ],
                                                className="shadow-sm",
                                                style={
                                                    "width": "100%", 
                                                    "height": "100%",
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                    }
                                            ),
                                            width={"size": 12, "md": 6},
                                            className="col-md-6 col-sm-12 mb-4"
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        html.H6("HISTÓRICO DEL REGISTRO DE POLLOS", className="text-center"),
                                                        style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dcc.Graph(id="chick-registration-weekly", config={"responsive": True},style={"height": "100%"}, className="h-100"),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "height": "50vh",
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        }, 
                                                    ),
                                                ],
                                                className="shadow-sm",
                                                style={
                                                    "width": "100%", 
                                                    "height": "100%",
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                    }
                                            ),
                                            width={"size": 12, "md": 6},
                                                className="col-md-6 col-sm-12 mb-4"
                                        ),
                                    ],
                                    className="mb-4",
                                ),
                                # Tablas
                                dbc.Row(
                                    [
                                        dbc.Col(  # Columna para la primera tarjeta
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(html.H6("CANTIDAD DE AVESTRUCES POR CORRAL", className="text-center"),
                                                    style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    html.Div(
                                                                        id="truzzy-grid",
                                                                        style={"overflowX": "auto"}  # Habilita el desplazamiento horizontal
                                                                    ),
                                                                    width=12
                                                                ),
                                                            ],
                                                            className="g-3",  # Espaciado entre las columnas                                                        
                                                        ),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px",
                                                        }, 
                                                    ),
                                                ],
                                                className="mb-4",  # Espaciado inferior entre tarjetas
                                                style= {
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"
                                                }
                                            ),
                                            width={"size": 12, "md": 6, "lg": 6},
                                            className="col-md-6 col-sm-12 mb-4" 
                                        ),
                                        dbc.Col(  # Columna para la segunda tarjeta
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(html.H6("CANTIDAD DE ALIMENTO POR TIPO", className="text-center"),
                                                    style={
                                                            "backgroundColor": "#1C5D3A",  # Fondo verde oscuro
                                                            "color": "white",  # Texto blanco
                                                            "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                                                            "padding": "10px",
                                                        },
                                                    ),
                                                    dbc.CardBody(
                                                        html.Div(id="food-grid", style={"overflowX": "auto"}),
                                                        style={
                                                            "backgroundColor": "#F5F5F5",  # Fondo gris claro
                                                            "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                                                            "padding": "20px"
                                                        }
                                                    ),
                                                ],
                                                className="shadow-sm",
                                                style={
                                                    "width": "100%", 
                                                    "height": "auto",
                                                    "border": "2px solid #528052",
                                                    "borderRadius": "15px"},
                                            ),
                                            width={"size": 12, "md": 6},
                                            className="col-md-6 col-sm-12 mb-4"                                            
                                        ),
                                    ],
                                    className="justify-content-center mb-4",  # Centrar las tarjetas en la fila
                                )
                            ],
                        ),
                    ],
                ),
            ],
            style={
            "backgroundColor": "#F5F5F5",  # Fondo general del dashboard
            "minHeight": "100vh",  # Altura mínima para cubrir la pantalla completa
            },
        )
        @callback(
            [
                Output("date-picker", "start_date"), 
                Output("date-picker", "end_date")
            ],
            [
                Input("quick-range", "value")
            ],
        )
        def update_dashboard(selected_range):
            if selected_range and selected_range in quick_ranges:
                start, end = quick_ranges[selected_range]
                return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
            return dash.no_update, dash.no_update


        @callback(
            [
                Output(config['html_id'], config['output_type']) for config in self.graph_configs.values()],
            [
                Input("url", "pathname"),
                Input("date-picker", "start_date"),
                Input("date-picker", "end_date")
            ],
        )
        def update_dashboard(pathname,start_date, end_date):
            try:
                self.logger.log_info(f'Start date: {start_date} , End date: {end_date}')
                triggered_id = [p["prop_id"] for p in callback_context.triggered][0]
                self.logger.log_info(triggered_id)
                
                today = dt.today() 
                figures = []
                for graph_key, config in self.graph_configs.items():
                    try:
                        if "url.pathname" in triggered_id:
                            data_results = self.fetch_data(graph_key, '20241101', today.strftime('%Y%m%d'))
                            self.data_results[graph_key] = data_results
                            func = self.graph_manager.get_func(config["function_name"])
                            
                            kwargs = {}
                            if config["trigger_dependent"] == True:
                                kwargs['start'] = start_date
                                kwargs['end'] = end_date
                            for arg in config["extra_arguments"]:
                                if arg.strip() == "warehouses_data":
                                    kwargs[arg] = self.const.warehouses_data
                            fig = func(*data_results, **kwargs)
                            figures.append(fig)
                        else:
                            kwargs = {}
                            if config["trigger_dependent"] == True:
                                self.logger.log_info(f"Recalculating graph (trigger dependent): {graph_key}")
                                data_results = self.data_results.get(graph_key)
                                kwargs['start'] = start_date
                                kwargs['end'] = end_date
                            else:
                                self.logger.log_info(f"Using cached result for graph (trigger independent): {graph_key}")
                                data_results = self.data_results.get(graph_key)        
                            
                            func = self.graph_manager.get_func(config["function_name"])
                            for arg in config["extra_arguments"]:
                                if arg.strip() == "warehouses_data":
                                    kwargs[arg] = self.const.warehouses_data

                            fig = func(*data_results, **kwargs)
                            figures.append(fig)

                    except Exception as ex:
                        self.logger.log_error(f"Error generating graph {graph_key}: {ex}")
                        traceback.print_exc()
                        figures.append(html.Div(f"Error loading {graph_key}"))

                return figures
            except Exception as ex:
                self.logger.log_error(f"Error updating dashboard: {ex}")
                return [html.Div("Error loading data")] * len(self.graph_configs)


        return layout
        
    
    def set_up(self):
        """
        Loads graph configurations from the `config.ini` file.

        Raises:
        -------
        FileNotFoundError:
            If the `config.ini` file is not found.
        """
        if getattr(sys, 'frozen', False):  # Si está empaquetado con PyInstaller
            base_path = sys._MEIPASS
        else:  # Si se está ejecutando en modo de desarrollo
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

        config_path = os.path.join(base_path, 'config.ini')
        if not os.path.exists(config_path):
            self.logger.log_error(f"No se encontró el archivo de configuración: {config_path}")
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")                          

        config = configparser.ConfigParser()
        config.read(config_path)

        for section in config.sections():
            if "function_name" in config[section]:
                self.graph_configs[section] = {
                    "function_name": config[section]["function_name"],
                    "query": config[section].get("query"),
                    "table_name": config[section].get("table_name"),
                    "params": config[section].get("params"),
                    "extra_arguments": config[section].get("extra_arguments", "").split(","),
                    "trigger_dependent": config[section].getboolean("trigger_dependent", False),
                    "html_id": config[section].get("html_id"),
                    "output_type": config[section].get("output_type")

                }

    def fetch_data(self, graph_key, start_date, end_date):
        """
        Fetches data from the API for a specific graph configuration.

        Args:
        -----
        graph_key (str): 
            The key identifying the graph configuration.
        start_date (str): 
            The start date for fetching data in "YYYY-MM-DD" format.
        end_date (str): 
            The end date for fetching data in "YYYY-MM-DD" format.

        Returns:
        --------
        list[pd.DataFrame]: 
            A list of DataFrames containing the fetched data.

        Raises:
        -------
        ValueError:
            If the graph configuration is not found.
        """
        config = self.graph_configs.get(graph_key)
        today = dt.today().strftime("%Y%m%d")

        if not config:
            self.logger.log_error(f"No configuration found for graph: {graph_key}")
            return pd.DataFrame()

        queries = config["query"].split(",")
        tables = config["table_name"].split(",")
        params = config["params"]
        data_results = []

        # Reemplazar dinámicamente las variables en los parámetros
        if params:
            params = params.format(start_date=start_date.replace("-",""), end_date=end_date.replace("-",""), today = today)
            
        for i, query in enumerate(queries):
            table_name = tables[i] if i < len(tables) else None
            # Ejecutar la consulta a la API
            data = self.agrotech_api.execute_query(query, table_name= table_name, params= params)
            data_results.append(data)
        
        return data_results

try:
    register_page(__name__, name = "Dashboard", path = '/')
    api = ApiClient()
    api.login() 
    constants = Constant(api)
    dashboard = Dashboard(constants)
    layout = dashboard.start()
except PageError as ex:
    pass