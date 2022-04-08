from flask import current_app as app

# Dash
import dash
import time
import pandas as pd

import plotly.express as px
import sys
import numpy as np

# colorcet
import colorcet as cc
from colorcet import kbc

kbc_r = kbc[::-1]
fire = cc.fire[5:]

colormaps = [kbc_r, fire, "Greens"]

# sys.path.append("../schema")
import mongoconfig
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State, ALL, State, MATCH, ALLSMALLER
from dash_extensions.enrich import Dash, Output, Input, Trigger, ServersideOutput
from dash.exceptions import PreventUpdate
import dash_table
from plotly.data import iris


from holoviews.operation.datashader import datashade
import holoviews.operation.datashader as hd
from holoviews import opts
from holoviews.plotting.util import process_cmap

import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash

hv.extension("plotly")

color_list = [
    "#000000",
    "#380000",
    "#560000",
    "#760100",
    "#980300",
    "#bb0600",
    "#df0d00",
    "#f93500",
    "#fe6800",
    "#ff9100",
    "#ffb402",
    "#ffd407",
    "#fff324",
]


def createDashApp(dsApp):

    # 처음부터 Layout에 넣어두면 작동함
    # Load iris dataset and replicate with noise to create large dataset

    df_original = iris()[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    df = pd.concat(
        [df_original + np.random.randn(*df_original.shape) * 0.1 for i in range(10000)]
    )
    dataset = hv.Dataset(df)

    # Build selection linking object
    selection_linker = hv.selection.link_selections.instance()

    scatter = selection_linker(
        hv.operation.datashader.datashade(
            hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"]),
            cmap=kbc_r,
        )
    ).opts(title="Datashader with %d points" % len(dataset))

    hist = selection_linker(
        hv.operation.histogram(dataset, dimension="petal_width", normed=False)
    )

    # Use plot hook to set the default drag mode to vertical box selection
    def set_hist_dragmode(plot, element):
        fig = plot.state
        fig["layout"]["dragmode"] = "select"
        fig["layout"]["selectdirection"] = "h"

    hist.opts(opts.Histogram(hooks=[set_hist_dragmode]))

    components = to_dash(dsApp, [scatter, hist], reset_button=True)

    ## dsApp.layout = html.Div(components.children)

    dsApp.layout = html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H1(
                                    "Datashader Graph Builder ",
                                    className="text-center text-primary mb-4",
                                ),
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Button("Query data", id="btn"),
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        children=[
                                            html.Button(
                                                "Add Chart",
                                                id="add-chart",
                                                n_clicks=0,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    # Data Setting
                                    dcc.Loading(
                                        dcc.Store(id="store"),
                                        fullscreen=True,
                                        type="dot",
                                    ),
                                    html.Div(
                                        id="container",
                                        children=[],
                                    ),
                                    html.Div(
                                        id="subContainer",
                                        children=[],
                                    ),
                                    # html.Div(
                                    #     id="subContainer",
                                    # ),
                                    html.Div(components.children),  # 그래프 2개
                                ]
                            )
                        ]
                    ),
                ]
            )
        )
    )
    ###############################################################
    @dsApp.callback(
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
                dcc.Dropdown(id="xVariable", value=None),
                dcc.Dropdown(id="yVariable", value=None, multi=True),
                html.Button(
                    "Draw",
                    id="updateBtn",
                    n_clicks=0,
                ),
            ],
        )
        div_children.append(new_child)
        return div_children

    @dsApp.callback(
        ServersideOutput("store", "data"), Trigger("btn", "n_clicks"), memoize=True
    )
    def query_data():
        time.sleep(1)

        # df = mongoconfig.loadSingleDataset(
        #     "project 1",
        #     "incheon",
        #     "none",
        #     [
        #         "ts",
        #         "700FIC028_Y",
        #         "700II781C_Y",
        #         "700II782C_Y",
        #         "700II783C_Y",
        #         "700LI770B_Y",
        #     ],
        # )
        # df = pd.json_normalize(df)

        df_original = iris()[
            ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        ]
        df = pd.concat(
            [
                df_original + np.random.randn(*df_original.shape) * 0.1
                for i in range(100)
            ]
        )

        return df

    # Dropdown X
    @dsApp.callback(Output("xVariable", "options"), Input("store", "data"))
    def update_x_dropdown(df):
        return [{"label": column, "value": column} for column in df]

    # Dropdown Y
    @dsApp.callback(Output("yVariable", "options"), Input("store", "data"))
    def update_y_dropdown(df):
        return [{"label": column, "value": df.columns.get_loc(column)} for column in df]

    # Update Graph
    @dsApp.callback(
        Output("subContainer", "children"),
        Input("store", "data"),
        Input("updateBtn", "n_clicks"),
        State("xVariable", "value"),
        State("yVariable", "value"),
        State("subContainer", "children"),
    )
    def update_graph(df, updateBtn, xVariable, yVariable, div_children):
        df2 = hv.Dataset(df)
        if updateBtn is 0:
            raise PreventUpdate
        if len(div_children) > 0:
            div_children = []
        layout = None
        allGraphs = None

        for index, column in enumerate(df.columns[yVariable]):
            xdim = hv.Dimension(xVariable)
            ydim = hv.Dimension(column)
            pts = hv.Scatter(
                df2,
                xdim,
                ydim,
                # kdims=[xVariable],
                # vdims=[column],
            )

            scatter = datashade(
                # pts, cmap=process_cmap(cc.b_linear_kryw_0_100_c71, provider=cc)
                pts,
                cmap=colormaps[index],
            ).opts(title="Datashader with %d points" % len(df))
            if allGraphs == None:
                allGraphs = scatter
            else:
                allGraphs = scatter * allGraphs

            # layout = (scatter * scatter2).opts(opts.Points(height=400, width=400))

        # hist = hv.operation.histogram(df, dimension="petal_length", normed=False)

        # scatter = pts.opts(title="Datashader")
        # scatter = scatter.opts(color="sepal_width")

        layout = (allGraphs).opts(
            opts.Points(height=400, width=400),
        )
        components = to_dash(dsApp, [layout], reset_button=True)
        div_children.append(html.Div(components.children))

        return div_children

    return dsApp
