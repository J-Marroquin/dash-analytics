import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt, timedelta as td
from typing import Tuple

def filters_card()->Tuple[dbc.Container,dict]:
    """
    Creates a card component with date range filters and quick range options for a dashboard.
    The card is styled with a header and body, featuring rounded borders, specific background colors, and padding
    for a clean user interface.

    Returns:
    --------
    A tuple containing the following:
    - Container:
        The card component with date filters.
    - dict:
        A dictionary mapping quick range labels to their corresponding date range tuples (start_date, end_date).
    """
    # Opciones rápidas de rango de tiempo
    quick_ranges = {
        "Últimos 7 días": (dt.now() - td(days=7), dt.now()),
        "Últimos 30 días": (dt.now() - td(days=30), dt.now()),
        "Último Año": (dt.now() - td(days=365), dt.now()),
    }

    _filters_card = dbc.Container(
        dbc.Card(
            [
                dbc.CardHeader(
                    html.H6("Selecciona un rango de fechas", className="text-center mb-0"),
                    style={
                        "backgroundColor": "#1C5D3A",  # Color de fondo verde oscuro
                        "color": "white",  # Texto blanco
                        "borderRadius": "10px 10px 0 0",  # Bordes superiores redondeados
                        "padding": "10px",
                    },
                ),
                dbc.CardBody(
                    dbc.Row(
                        [
                            # DatePickerRange
                            dbc.Col(
                                [
                                    dbc.Label("Fecha", html_for="date-picker", className="d-block mb-1"),
                                    dcc.DatePickerRange(
                                        id="date-picker",
                                        calendar_orientation="horizontal",
                                        start_date=(dt.now() - td(days=7)).strftime("%Y-%m-%d"),
                                        end_date=dt.now().strftime("%Y-%m-%d"),
                                        display_format="DD/MM/YYYY",
                                        first_day_of_week=1,
                                        min_date_allowed=dt(2024, 11, 1),
                                        minimum_nights=1,
                                        updatemode="singledate",
                                    ),
                                ],
                                width=6,  # Ancho proporcional
                                className="p-0",
                            ),
                            # Select and Search (dbc.Select)
                            dbc.Col(
                                [
                                    dbc.Label("Rango Rápido", html_for="date-picker", className="d-block mb-1"),
                                    dbc.Select(
                                        id="quick-range",
                                        options=[{"label": k, "value": k} for k in quick_ranges.keys()],
                                        placeholder="Selecciona un rango",
                                    ),
                                ],
                                width=6,  # Ancho proporcional
                                className="p-2",
                            ),
                        ],
                        className="align-items-center g-3",  # Espaciado y alineación vertical
                    ),
                    style={
                        "backgroundColor": "#F5F5F5",  # Fondo gris claro
                        "borderRadius": "0 0 14px 14px",  # Bordes inferiores redondeados
                        "padding": "10px",
                    },
                ),                
            ],
            className="bg-light",  
            style={
                "border": "2px solid #528052",
                "borderRadius": "15px",  # Bordes redondeados
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                "width": "100%",
                "maxWidth": "600px",
            },
        ),
        fluid=True,
    )

    return _filters_card, quick_ranges




