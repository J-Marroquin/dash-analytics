import pandas as pd
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta as td
from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.api_client import ApiClient
from DashboardAgrotechApp.graphs.empty_fig import create_empty_fig

def plot_material_revaluation(food_exit_data: pd.DataFrame, reproduccion_data: pd.DataFrame, warehouses_data:pd.DataFrame, start:str, end:str)->go.Figure:
    """
    Generates a horizontal bar chart showing the material revaluation based on food exit and reproduction data.

    This function combines data from food exits and reproduction entries, aligns it with warehouse information, filters it
    by a specified date range, and calculates total consumption (`LineTotal`) and quantities grouped by item description
    and warehouse name. It then visualizes the data in a stacked bar chart.

    Args:
    -----
        food_exit_data (pd.DataFrame): 
            A DataFrame containing data on food exits with columns:
            - `DocNum`, `DocDate`, `Ref2`, `WhsCode`, `ItemCode`, `Dscription`, `Quantity`, `LineTotal`.
        reproduccion_data (pd.DataFrame): 
            A DataFrame containing reproduction data with the same structure as `food_exit_data`.
        warehouses_data (pd.DataFrame): 
            A DataFrame with warehouse information containing columns `WhsCode` and `WhsName`.
        start (str): 
            The start date of the range in the format 'YYYY-MM-DD'.
        end (str): 
            The end date of the range in the format 'YYYY-MM-DD'.

    Returns:
    --------
        plotly.graph_objects.Figure: 
            A Plotly bar chart showing material revaluation grouped by item and warehouse.
        None: 
            If an exception occurs during the process, logs the error and returns a placeholder figure.

    Notes:
        - The chart uses custom colors for specific warehouse stages (e.g., `DESARROLLO`, `ENGORDA`, `REPRODUCCIÓN`).
        - Missing dates in the input data are handled gracefully.
        - Returns an empty placeholder chart if input data is empty.

    Raises:
    -------
    ValueError: 
        If the `start` or `end` dates are not in the correct format.
    """

    if food_exit_data.empty:
        return create_empty_fig("No hay datos disponibles")
    if reproduccion_data.empty:
        return create_empty_fig("No hay datos disponibles")
    
    logger = Logger()
    api = ApiClient()
    api.login()
    try:
        start_date = pd.to_datetime(start, format="%Y-%m-%d")
        end_date = pd.to_datetime(end, format="%Y-%m-%d")       
        reproduccion_data['Ref2'] = 0
        reproduccion_data['WhsCode'] = 'RAN09'
        column_order = ["DocNum", "DocDate", "Ref2", "WhsCode", "ItemCode", "Dscription", "Quantity", "LineTotal"]
        reproduccion_data = reproduccion_data[column_order] 

        combined_df = pd.concat([food_exit_data, reproduccion_data],ignore_index= True)
        combined_df = combined_df.merge(warehouses_data,how='left', on='WhsCode')
        combined_df['DocDate'] = pd.to_datetime(combined_df['DocDate'],format= "%Y%m%d")
        combined_df['LineTotal'] = combined_df['LineTotal'].astype(float)
        combined_df['Quantity'] = combined_df['Quantity'].astype(float) 
        filtered_df = combined_df[(combined_df["DocDate"] >= start_date) & (combined_df["DocDate"] <= end_date)]
        df_grouped = filtered_df.groupby(["Dscription", "WhsName"], as_index=False).agg({"LineTotal": "sum", "Quantity": "sum"})
        fig = px.bar(
            df_grouped,
            x="LineTotal",          # Total de LineTotal en el eje X
            y="Dscription",         # Descripción del artículo en el eje Y
            color="WhsName",        # Colores basados en el almacén
            orientation="h",        # Barras horizontales
            text="LineTotal",  # Texto con formato de LineTotal
            labels={
                "Dscription": "Artículo",
                "LineTotal": "Total consumido",
                "WhsName": "Almacén",
            },
            template= "seaborn"
        )
        # Personalizamos el diseño
        fig.update_layout(
            barmode="stack",       # Apilado
            xaxis_title="Total",
            yaxis_title="Descripción del Artículo",
            showlegend=True,       # Mostrar leyenda
            legend=dict(
                title="ETAPA",
                orientation="h",               # Horizontal
                y=1.2,                        # Posición vertical por encima del gráfico
                x=0.5,                         # Centrar horizontalmente
                xanchor="center",
                yanchor="top",
            ),
            plot_bgcolor="#F5F5F5",
            paper_bgcolor="#F5F5F5",
        )

        custom_colors = {
            "DESARROLLO": "#41A047", 
            "ENGORDA": "#1C5D3A", 
            "REPRODUCCIÓN": "#7A9F41",  
        }

        fig.for_each_trace(lambda trace: trace.update(marker=dict(color=custom_colors.get(trace.name, "#999999"))))
        # Ajustamos el formato del texto en las barras
        fig.update_traces(texttemplate="$%{x:,}", textposition="inside")
        return fig
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in material_revaluation module: {ex}")
        return create_empty_fig("Something went wrong!")   



if __name__ == "__main__":
    api= ApiClient()
    api.login()
    food_exit_df = api.execute_query("query28",table_name = "OMRV", params='&startdate=20241201&enddate=20250115&pagesize=500&pagenumber1')
    reproduccion_food_exit = api.execute_query("query29", table_name = "OIGE",params='&startdate=20241201&enddate=20250115&pagesize=500&pagenumber1')
    fig = plot_material_revaluation(food_exit_data=food_exit_df, reproduccion_data= reproduccion_food_exit, start="20241223", end="20250105")
    fig.show()