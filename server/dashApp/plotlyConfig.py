from flask import current_app as app

# Dash
import dash
import time
import pandas as pd

import plotly.express as px
import sys

# sys.path.append("../schema")
import mongoconfig
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State, ALL, State, MATCH, ALLSMALLER
from dash_extensions.enrich import Dash, Output, Input, Trigger, ServersideOutput
from dash.exceptions import PreventUpdate
import dash_table
from plotly.data import iris


def createDashApp(plotlyApp):
    plotlyApp.layout = html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Plotly Graph Builder ",
                                    className="text-center text-primary mb-4",
                                ),
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            # Data Setting
                            html.Button("Query data", id="btn"),
                            dcc.Loading(
                                dcc.Store(id="store"), fullscreen=True, type="dot"
                            ),
                            html.Div(
                                children=[
                                    html.Button(
                                        "Add Chart", id="add-chart", n_clicks=0
                                    ),
                                ]
                            ),
                            html.Div(
                                id="container",
                                children=[],
                            ),
                        ]
                    ),
                ]
            )
        )
    )

    @plotlyApp.callback(
        Output("container", "children"),
        [Input("add-chart", "n_clicks")],
        [State("container", "children")],
    )
    def display_graphs(n_clicks, div_children):

        new_child = html.Div(
            style={
                "width": "45%",
                "display": "inline-block",
                "outline": "thin lightgrey solid",
                "padding": 10,
            },
            children=[
                dcc.Dropdown(id={"type": "xVariable", "index": n_clicks}, value=None),
                dcc.Dropdown(
                    id={"type": "yVariable", "index": n_clicks}, value=None, multi=True
                ),
                html.Button(
                    "Draw",
                    id={"type": "updateBtn", "index": n_clicks},
                    n_clicks=0,
                ),
                dcc.Graph(
                    id={"type": "graph", "index": n_clicks},
                ),
            ],
        )
        div_children.append(new_child)
        return div_children

    @plotlyApp.callback(
        ServersideOutput("store", "data"), Trigger("btn", "n_clicks"), memoize=True
    )
    def query_data():
        time.sleep(1)

        df = mongoconfig.loadSingleDataset(
            "project 1",
            "incheon",
            "none",
            [
                "ts",
                "700FIC028_Y",
                "700II781C_Y",
                "700II782C_Y",
                "700II783C_Y",
                "700LI770B_Y",
            ],
        )
        df = pd.json_normalize(df)
        # df = iris()
        return df

    # Dropdown X
    @plotlyApp.callback(
        Output({"type": "xVariable", "index": MATCH}, "options"), Input("store", "data")
    )
    def update_x_dropdown(df):
        return [{"label": column, "value": column} for column in df]

    # Dropdown Y
    @plotlyApp.callback(
        Output({"type": "yVariable", "index": MATCH}, "options"), Input("store", "data")
    )
    def update_y_dropdown(df):
        return [{"label": column, "value": df.columns.get_loc(column)} for column in df]

    # Update Graph
    @plotlyApp.callback(
        Output({"type": "graph", "index": MATCH}, "figure"),
        [
            Input("store", "data"),
            Input({"type": "updateBtn", "index": MATCH}, "n_clicks"),
            State({"type": "xVariable", "index": MATCH}, "value"),
            State({"type": "yVariable", "index": MATCH}, "value"),
        ],
    )
    def update_graph(df, updateBtn, xValue, yValue):
        # ctx = dash.callback_context
        # btnType = eval(ctx.triggered[0]["prop_id"].split(".")[0])["type"]
        # if update_plotly is 0:
        #     raise PreventUpdate
        fig = px.scatter(df, x=xValue, y=df.columns[yValue], title="Incheon Data")
        fig.update_traces(marker={"size": 5})
        return fig

    return plotlyApp
