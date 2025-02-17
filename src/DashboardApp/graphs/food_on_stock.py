import pandas as pd
import dash_ag_grid as dag
from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.graphs.empty_fig import create_empty_fig

def plot_food_grid(data: pd.DataFrame):
    """
    Creates an interactive grid displaying available food stock information.

    This function processes the input data to prepare it for display in an AgGrid component.
    The grid includes columns for food item names and their available quantities, which are
    rounded to two decimal places.

    Args:
    -----
    data (pd.DataFrame): 
        A DataFrame containing food stock data with columns:
        - `ItemName` (str): The name of the food item.
        - `OnHand` (float): The available stock of the food item.
        - Optional: `ItemCode`, `SWeight1` (dropped if present).

    Returns:
    --------
        dash_ag_grid.AgGrid: An interactive grid component displaying the available food stock.
        plotly.graph_objects.Figure: A placeholder figure if an exception occurs.

    Notes:
        - The grid allows sorting, filtering, and resizing of columns.
        - Columns for `ItemCode` and `SWeight1` are ignored if present in the input data.
        - The grid adjusts column sizes automatically and has a predefined style.

    Raises:
    -------
    ValueError: 
        If the input data is not in the expected format or an error occurs during processing.
    """
    logger = Logger()
    try: 
        data.drop(columns = ['ItemCode', 'SWeight1'], inplace= True, errors='ignore')
        data['OnHand'] = data["OnHand"].astype(float)
        data['OnHand'] = data["OnHand"].round(2)

        columnDefs = [
        {"headerName": "Alimento", "field": "ItemName"},
        {"headerName": "Disponible", "field": "OnHand"}
        ]
        
        grid = dag.AgGrid(
            id = 'food-on-stock',
            columnDefs = columnDefs,
            rowData = data.to_dict("records"),
            columnSize = "autoSize",
            defaultColDef={"sortable": True, "filter": True, "resizable": True},  # Propiedades comunes
            style={"height": "430px", "width": "100%"}
        )
        return grid
    except Exception as ex:
        logger.log_error(f"Error plotting the grid in food_on_stock module: {ex}")
        return create_empty_fig("No hay datos disponibles")
    