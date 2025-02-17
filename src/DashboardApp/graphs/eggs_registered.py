import locale
from datetime import datetime as dt, timedelta as td
import calendar
import math
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
from DashboardAgrotechApp.logger import Logger



def plot_monthly_eggs_alert(this_month_eggs_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of eggs collected for the current month.

    Args:
    -----
    this_month_eggs_df (pd.DataFrame): 
        A DataFrame containing the total eggs for the current month in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the monthly total and current month.

    Raises:
    -------
    Exception:
        Logs an error if an exception occurs.
    """
    logger = Logger()
    locale.setlocale(locale.LC_TIME, "Spanish_Mexico")    
    try:
        this_month_eggs = this_month_eggs_df.loc[0,"Col1"]
        this_month_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ESTE MES **
            ### {this_month_eggs}
            {dt.today().strftime("%B").upper()}
            """
        ), color= "#7A9F41")  
        return this_month_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")
    

def plot_season_eggs_alert(total_eggs_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of eggs collected for the current season.

    Args:
    -----
    total_eggs_df (pd.DataFrame): 
        A DataFrame containing the total eggs for the season in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total eggs and season year(s).

    Raises:
    -------
    Exception:
        Logs an error if an exception occurs.
    """
    logger = Logger()
    try:
        total_eggs = total_eggs_df.loc[0,"Col1"]
        today = dt.today()
        current_year = today.year
        if today < dt(today.year,11,1):
            last_year = current_year - 1
            nom = f'{last_year}/{current_year}'
        else:
            next_year = current_year + 1
            nom = f'{current_year}/{next_year}'
        
        total_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** TOTAL**
            ### {total_eggs}
            {nom}
            """
        ), color= "#7A9F41")    
        return total_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")


def plot_yesterday_eggs_alert(yesterday_eggs_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of eggs collected yesterday.

    Args:
    -----
    yesterday_eggs_df (pd.DataFrame): 
        A DataFrame containing the total eggs collected yesterday in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total eggs and yesterday's date.

    Raises:
    -------
    Exception: 
        Logs an error if an exception occurs.
    """
    logger = Logger()
    try:
        yesterday_eggs = yesterday_eggs_df.loc[0,"Col1"]
        yesterday = dt.today() - td(days=1)
        yesterday_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** AYER **
            ### {yesterday_eggs}
            {yesterday.strftime('%d-%m-%Y')}
            """
        ), color= "#7A9F41") 

        return yesterday_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")
        return None   

def plot_day_before_yesterday_eggs_alert(before_yesterday_eggs_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of eggs collected the day before yesterday.

    Args:
    -----
    before_yesterday_eggs_df (pd.DataFrame): 
        A DataFrame containing the total eggs collected the day before yesterday in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total eggs and the day before yesterday's date.

    Raises:
    -------
    Exception:
        Logs an error if an exception occurs.
    """

    logger = Logger()
    try:
        before_yesterday_eggs = before_yesterday_eggs_df.loc[0,"Col1"]
        before_yesterday = dt.today() - td(days=2)
        before_yesterday_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ANTEAYER **
            ### {before_yesterday_eggs}
            {before_yesterday.strftime('%d-%m-%Y')}
            """
        ), color= "#7A9F41") 

        return before_yesterday_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")
        return None       


def plot_last_30_days_eggs(last_30_days_eggs_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of eggs collected in the last 30 days.

    Args:
    -----
    last_30_days_eggs_df (pd.DataFrame): 
        A DataFrame containing the total eggs collected in the last 30 days in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total eggs for the last 30 days.

    Raises:
    -------
    Exception: 
        Logs an error if an exception occurs.
    """
    logger = Logger()
    locale.setlocale(locale.LC_TIME, "Spanish_Mexico")    
    try:
        monthly_eggs = last_30_days_eggs_df.loc[0,"Col1"]
        montly_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ÚLTIMOS 30 **
            ### {monthly_eggs}
            DÍAS
            """
        ), color= "#7A9F41")  
        return montly_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")

def plot_end_month_forecast_eggs(data:pd.DataFrame):
    """
    Generates an alert displaying the forecasted total number of eggs for the end of the current month.

    Args:
    -----
    data (pd.DataFrame): 
        A DataFrame containing daily egg collection data with columns:
        - `U_ReceptionDate` (datetime): The date of egg reception.
        - `Col2` (int): The number of eggs collected.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the forecasted total eggs for the current month.

    Raises:
    -------
    Exception: 
        Logs an error if an exception occurs.
    """
    logger = Logger()
    today = dt.today()
    start_date = dt(today.year,today.month,1)
    _, last_day = calendar.monthrange(today.year, today.month)
    end_date = dt(today.year, today.month, last_day)


    date_range = pd.date_range(start=start_date,end=end_date)
    calendar_df = pd.DataFrame({'U_ReceptionDate': date_range})
    calendar_df['U_ReceptionDate'] = pd.to_datetime(calendar_df['U_ReceptionDate'].dt.date)
    data.rename(columns={'Col2': 'Huevos'}, inplace=True)
    data['U_ReceptionDate'] = pd.to_datetime(data['U_ReceptionDate'], format='%Y%m%d')
    data['Huevos'] = data['Huevos'].astype(int)
    data_filtered = data[(data['U_ReceptionDate'] >= start_date) & (data['U_ReceptionDate'] < today)]
    mean = data_filtered['Huevos'].mean()
    data_copy = pd.merge(calendar_df, data, on = 'U_ReceptionDate', how='left').fillna(mean)
    forecast = data_copy['Huevos'].sum()
    try:
        forecast_eggs_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ESTIMACIÓN **
            ### {math.floor(forecast)}
            FIN DE MES
            """
        ), color= "#7A9F41")  
        return forecast_eggs_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in weekly_egg_registration_graph module: {ex}")
    
if __name__ == "__main__":
    pass