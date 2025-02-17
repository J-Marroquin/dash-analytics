import os
import sys
import configparser
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, register_page

register_page(__name__, name = "login", path = '/login')

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Img(
                                src="https://44e62736-28ca-4ccb-982c-f5151e678df0.avestruz.mx/logo.svg", 
                                style={
                                    "width": "150px",
                                    "margin": "auto",
                                    "display": "block",
                                    "margin-bottom": "20px",
                                },
                            ),
                            html.H2(
                                "Bienvenido",
                                style={"text-align": "center", "margin-bottom": "20px"},
                            ),
                            dbc.Form(
                                [
                                    dbc.Label("Usuario", html_for="user-input"),
                                    dbc.Input(
                                        id="user-input",
                                        type="text",
                                        placeholder="Usuario",
                                        className="mb-3",
                                    ),
                                    dbc.Label("Contraseña", html_for="password-input"),
                                    dbc.Input(
                                        id="password-input",
                                        type="password",
                                        placeholder="Contraseña",
                                        className="mb-3",
                                    ),
                                    dbc.Button(
                                        "Iniciar sesión",
                                        color="success",
                                        className="w-100",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    style={"width": "400px", "margin": "auto", "padding": "20px"},
                )
            )
        )
    ],
    fluid=True,
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh",
    },
)
@callback(
    Output("session-auth", "data"),
    Output("url", "pathname"),
    Input("login-button", "n_clicks"),
    State("user-input", "value"),
    State("password-input", "value"),
    prevent_initial_call=True,
)
def login_user(n_clicks, username, password):
    config=configparser.ConfigParser()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    config.read(os.path.join(base_path,'config.ini'))
    if username == "admin" and password == "password":  # Sustituir con lógica real
        return {"authenticated": True}, "/"
    return {"authenticated": False}, "/login"


