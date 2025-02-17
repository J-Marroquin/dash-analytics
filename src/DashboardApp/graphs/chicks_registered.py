import locale
from datetime import datetime as dt, timedelta as td
import calendar
import math
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
from DashboardAgrotechApp.logger import Logger



def plot_monthly_chicks_alert(this_month_chicks_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of chickens entry for the current month.

    Args:
    -----
    this_month_chicks_df (pd.DataFrame): 
        A DataFrame containing the total chickens for the current month in the column `Col1`.

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
        this_month_chicks = this_month_chicks_df.loc[0,"Col1"]
        this_month_chicks_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ESTE MES **
            ### {this_month_chicks}
            {dt.today().strftime("%B").upper()}
            """
        ), color= "#41A047")  
        return this_month_chicks_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")
    

def plot_season_chicks_alert(total_chicks_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of chicks collected for the current season.

    Args:
    -----
    total_chicks_df (pd.DataFrame): 
        A DataFrame containing the total chicks for the season in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total chicks and season year(s).

    Raises:
    -------
    Exception:
        Logs an error if an exception occurs.
    """
    logger = Logger()
    try:
        total_chicks = total_chicks_df.loc[0,"Col1"]
        today = dt.today()
        current_year = today.year
        if today < dt(today.year,11,1):
            last_year = current_year - 1
            nom = f'{last_year}/{current_year}'
        else:
            next_year = current_year + 1
            nom = f'{current_year}/{next_year}'
        
        total_chicks_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** TOTAL**
            ### {total_chicks}
            {nom}
            """
        ), color= "#41A047")    
        return total_chicks_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")


def plot_yesterday_chicks_alert(yesterday_chicks_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of chicks registered yesterday.

    Args:
    -----
    yesterday_chicks_df (pd.DataFrame): 
        A DataFrame containing the total chickens registered yesterday in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total chicks and yesterday's date.

    Raises:
    -------
    Exception: 
        Logs an error if an exception occurs.
    """
    logger = Logger()
    try:
        yesterday_chicks = yesterday_chicks_df.loc[0,"Col1"]
        yesterday = dt.today() - td(days=1)
        yesterday_chicks_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** AYER **
            ### {yesterday_chicks}
            {yesterday.strftime('%d-%m-%Y')}
            """
        ), color= "#41A047") 

        return yesterday_chicks_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")
        return None   

def plot_day_before_yesterday_chicks_alert(before_yesterday_chicks_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of chickens registered the day before yesterday.

    Args:
    -----
    before_yesterday_chicks_df (pd.DataFrame): 
        A DataFrame containing the total chickens registered the day before yesterday in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total chickens and the day before yesterday's date.

    Raises:
    -------
    Exception:
        Logs an error if an exception occurs.
    """

    logger = Logger()
    try:
        before_yesterday_chicks = before_yesterday_chicks_df.loc[0,"Col1"]
        before_yesterday = dt.today() - td(days=2)
        before_yesterday_chicks_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ANTEAYER **
            ### {before_yesterday_chicks}
            {before_yesterday.strftime('%d-%m-%Y')}
            """
        ), color= "#41A047") 

        return before_yesterday_chicks_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")
        return None       


def plot_last_30_days_chicks(last_30_days_chicks_df:pd.DataFrame):
    """
    Generates an alert displaying the total number of chickens registered in the last 30 days.

    Args:
    -----
    last_30_days_chicks_df (pd.DataFrame): 
        A DataFrame containing the total chickens registered in the last 30 days in the column `Col1`.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the total chickens for the last 30 days.

    Raises:
    -------
    Exception: 
        Logs an error if an exception occurs.
    """
    logger = Logger()
    locale.setlocale(locale.LC_TIME, "Spanish_Mexico")    
    try:
        monthly_chickens = last_30_days_chicks_df.loc[0,"Col1"]
        montly_chickens_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ÚLTIMOS 30 **
            ### {monthly_chickens}
            DÍAS
            """
        ), color= "#41A047")  
        return montly_chickens_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")

def plot_end_month_forecast_chicks(data:pd.DataFrame):
    """
    Generates an alert displaying the forecasted total number of chickens for the end of the current month.

    Args:
    -----
    data (pd.DataFrame): 
        A DataFrame containing daily chick collection data with columns:
        - `U_DayOfBirth` (datetime): The date of chicken birth.
        - `Col2` (int): The number of chicks registered.

    Returns:
    --------
    dash_bootstrap_components.Alert: 
        An alert component showing the forecasted total chickens for the current month.

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
    calendar_df = pd.DataFrame({'U_DayOfBirth': date_range})
    calendar_df['U_DayOfBirth'] = pd.to_datetime(calendar_df['U_DayOfBirth'].dt.date)
    data.rename(columns={'Col2': 'Pollos'}, inplace=True)
    data['U_DayOfBirth'] = pd.to_datetime(data['U_DayOfBirth'], format='%Y%m%d')
    data['Pollos'] = data['Pollos'].astype(int)
    data_filtered = data[(data['U_DayOfBirth'] >= start_date) & (data['U_DayOfBirth'] < today)]
    mean = data_filtered['Pollos'].mean()
    data_copy = pd.merge(calendar_df, data, on = 'U_DayOfBirth', how='left').fillna(mean)
    forecast = data_copy['Pollos'].sum()
    try:
        forecast_chicks_alert = dbc.Alert(dcc.Markdown(
            f"""
            ** ESTIMACIÓN **
            ### {math.floor(forecast)}
            FIN DE MES
            """
        ), color= "#41A047")  
        return forecast_chicks_alert
    except Exception as ex:
        logger.log_error(f"Error plotting the graph in chicks_registered module: {ex}")
    
if __name__ == "__main__":
    pass