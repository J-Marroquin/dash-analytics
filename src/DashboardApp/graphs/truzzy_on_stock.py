import pandas as pd
import dash_ag_grid as dag

from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.api_client import ApiClient
from DashboardAgrotechApp.graphs.empty_fig import create_empty_fig

def plot_truzzy_grid(data: pd.DataFrame, warehouses_data:pd.DataFrame):
    """
    Creates an interactive grid showing the current stock of items by warehouse.

    This function merges the input data with warehouse data, calculates the total stock,
    and renders the data in an AgGrid component. The grid includes sortable, filterable,
    and resizable columns.

    Args:
    -----
    data (pd.DataFrame): 
        A DataFrame containing stock data with columns:
        - `WhsCode`: Warehouse code.
        - `OnStock`: Current stock quantity.
    warehouses_data (pd.DataFrame): 
        A DataFrame containing warehouse information with columns:
        - `WhsCode`: Warehouse code.
        - `WhsName`: Warehouse name.

    Returns:
    --------
    dash_ag_grid.AgGrid: 
        An interactive grid component displaying the stock by warehouse.
    plotly.graph_objects.Figure: 
        A placeholder figure if an exception occurs.

    Notes:
        - The grid includes a total row summarizing the stock across all warehouses.
        - The column definitions are preconfigured with sorting, filtering, and resizing enabled.
    """

    logger = Logger()
    try:
        data = data.merge(warehouses_data,how='left', on='WhsCode')
        data.drop(columns= ["WhsCode"], inplace= True)
        data = data[["WhsName", "OnStock"]] 
        total = data['OnStock'].astype(int).sum()
        data = pd.concat(
                [data, pd.DataFrame({"WhsName": ["TOTAL"], "OnStock": [total]})],
                ignore_index=True,
            )
        columnDefs = [
        {"headerName": "CORRAL", "field": "WhsName"},
        {"headerName": "HOY", "field": "OnStock", "type": "numericColumn"},
        ]
        
        grid = dag.AgGrid(
            id = 'truzzy-on-stock',
            columnDefs = columnDefs,
            rowData = data.to_dict("records"),
            defaultColDef={"sortable": True, "filter": True, "resizable": True},  # Propiedades comunes
            style={"height": "430px", "width": "100%"}
        )
        return grid
    except Exception as ex:
        logger.log_error(f"Error plotting the grid in truzzy_on_stock module: {ex}")
        return create_empty_fig("No hay datos disponibles")