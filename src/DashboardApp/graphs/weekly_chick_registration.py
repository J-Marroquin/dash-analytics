import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
import plotly.express as px
import plotly.graph_objects as go
from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.api_client import ApiClient

def plot_chicks_entry(data: pd.DataFrame,start:str,end:str)->go.Figure:
    """
    Generates a bar chart of chickens registration data over a specified date range.

    This function takes chick registration data, aligns it with a complete calendar date range,
    and produces a Plotly bar chart showing the number of chick registered per day.

    Args:
    -----
    data (pd.DataFrame): 
        A DataFrame containing egg registration data with the following columns:
        - `U_DayOfBirth` (str or datetime): The birth date of the chickens.
        - `Col2` (int): The number of chickens registered (renamed to 'Pollos').
    start (str): 
        The start date of the range in the format 'YYYY-MM-DD'.
    end (str): 
        The end date of the range in the format 'YYYY-MM-DD'.

    Returns:
    --------
        plotly.graph_objects.Figure: 
            A Plotly bar chart showing the number of chickens registered per day.
        None: 
            If an exception occurs during the process, logs the error and returns None.

    Raises:
    -------
        ValueError: If the `start` or `end` dates are not in the correct format.

    Notes:
        - The chart uses a green color for the bars (`#7A9F41`) and a clean design with a light gray background.
        - If there are missing dates in the data, they are filled with zero egg entries.
    """
    logger = Logger()
    try:
        start_date = dt.strptime(start,"%Y-%m-%d")
        end_date = dt.strptime(end,"%Y-%m-%d")

        date_range = pd.date_range(start=start_date,end=end_date)
        calendar_df = pd.DataFrame({'U_DayOfBirth': date_range})
        calendar_df['U_DayOfBirth'] = pd.to_datetime(calendar_df['U_DayOfBirth'].dt.date)
        data.rename(columns={'Col2': 'Pollos'}, inplace=True)
        data['U_DayOfBirth'] = pd.to_datetime(data['U_DayOfBirth'], format='%Y%m%d')
        data['Pollos'] = data['Pollos'].astype(int)

        data_copy = pd.merge(calendar_df, data, on = 'U_DayOfBirth', how='left').fillna(0)
        fig = px.bar(
            data_copy,
            x="U_DayOfBirth",
            y="Pollos",
            labels={"U_DayOfBirth": "Fecha", "Pollos": "Cantidad de Pollos Registrados"},
            template="seaborn",
        )

        fig.update_traces(marker_color="#7A9F41")
        # Personalizar el diseño
        fig.update_layout(
            xaxis=dict(tickformat="%Y-%m-%d", tickangle=45, showgrid=False),  # Formato y rotación de fechas
            yaxis_title="Cantidad de Pollos",
            xaxis_title="Fecha",
            plot_bgcolor="#F5F5F5",
            paper_bgcolor="#F5F5F5",
        )
        return fig
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_chick_registration module: {ex}")
        return None   

if __name__ == "__main__":
    api = ApiClient()
    api.login()
    data = api.execute_query("query43", table_name= "AGR_POLLOS", params="&startdate=20250120&enddate=20250210&pagesize=500&pagenumber=1")
    print(data)
    fig = plot_chicks_entry(data, start="20250215", end="20250210")
    fig.show()

