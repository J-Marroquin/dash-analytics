import locale
import pandas as pd
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta as td
from DashboardAgrotechApp.logger import Logger
from DashboardAgrotechApp.api_client import ApiClient
from DashboardAgrotechApp.graphs.empty_fig import create_empty_fig


def plot_food_purchase_history(data:pd.DataFrame)->go.Figure:
    """
    Generates a line chart representing monthly food purchase expenses.

    This function processes food purchase data, aggregates it by month, and creates a
    line chart with custom text labels showing the total expense for each month.

    Args:
    -----
    data (pd.DataFrame): A DataFrame containing food purchase data with columns:
        - `DocDate` (str or datetime): The document date of the purchase in '%Y%m%d' format.
        - `DocTotal` (float): The total cost of the purchase.

    Returns:
    --------
    plotly.graph_objects.Figure: 
        A Plotly line chart showing monthly food purchase expenses.

    Notes:
        - The chart uses custom text labels to display expense totals for alternating months.
        - Labels are formatted in millions (e.g., `$1.23M`) for clarity.
        - Spanish locale is set for month names in the x-axis.

    Raises:
    -------
    ValueError: 
        If `data` does not contain the required columns or if the date format is incorrect.
    """
    locale.setlocale(locale.LC_TIME, "Spanish_Mexico")
    data['DocDate'] = pd.to_datetime(data['DocDate'],format='%Y%m%d')
    data['DocTotal'] = data['DocTotal'].astype(float)
    data['Period'] = data['DocDate'].dt.to_period('M').astype(str)
    grouped_data = data.groupby('Period', as_index=False)['DocTotal'].sum()
    
    fig = px.line(
        grouped_data,
        x='Period',
        y='DocTotal',
        #title="GASTO MENSUAL EN COMPRAS DE ALIMENTO",
        labels={
            'Period': 'Período',
            'DocTotal': 'Total'
        },
        markers=False,
        template='seaborn'
    )

    text_labels = []
    show_label = True

    current_month = str(pd.Timestamp.now().to_period('M'))
    for period, x in zip(reversed(grouped_data['Period']), reversed(grouped_data['DocTotal'])):
        if period == current_month or show_label:
            text_labels.append(f'${x/1e6:.2f}M')  # Mostrar etiqueta
        else:
            text_labels.append('')  # No mostrar etiqueta
        show_label = not show_label  # Alternar True / False cada mes

    # Como el loop está en orden inverso, hay que revertir los labels para que coincidan con el dataframe
    text_labels.reverse()
    

    fig.update_traces(
        mode='lines+text',  # Mostrar línea y etiquetas de datos
        line_color = "#419F86",
        text = text_labels,
        textposition = ["top right" if i % 2 == 0 else "bottom left" for i in range(len(grouped_data))]
    )
    # Ajustar diseño del gráfico
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Gasto Mensual",
        title_x=0.5,  # Centrar título
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
    )

    return fig

if __name__ == "__main__":
    #data = pd.read_csv(r'C:\Users\jmarroquin\Downloads\compras.csv')
    api = ApiClient()
    api.login()
    data = api.execute_query("query32", "OPDN", params= "&Pagesize=500&pagenumber=1")
    plot_food_purchase_history(data)
    

