import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, register_page

register_page(__name__, name = "docs", path = '/docs')

layout = html.Div([
    html.H1("Agrotech Dashboard Documentation"),
    html.Iframe(
        src="/assets/sphinx_docs/index.html",  # Ruta al archivo HTML
        style={"width": "100%", "height": "100vh", "border": "none"}
    )
])