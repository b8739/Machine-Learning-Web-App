# # Dash
# import dash
# import time
# import pandas as pd

# import plotly.express as px
# import sys

# # sys.path.append("../schema")
# import mongoconfig
# import plotlyApp2

# dash.register_page(__name__, path="/edaApp/")
# from application import application
# from dash import Dash, dcc, html, callback
# from dash.dependencies import Input, Output, State, ALL, State, MATCH, ALLSMALLER
# from dash_extensions.enrich import Dash, Output, Input, Trigger, ServersideOutput
# from dash.exceptions import PreventUpdate
# import dash_table
# from plotly.data import iris


# #####################################################################################


# layout = html.Div(
#     [
#         # Data Setting
#         # html.Button("Query data", id="btn"),
#         # dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot"),
#         html.Div(
#             children=[
#                 html.Button("Add Chart", id="add-chart", n_clicks=0),
#             ]
#         ),
#         html.Div(id="container", children=[]),
#     ]
# )


# @callback(
#     Output("container", "children"),
#     [Input("add-chart", "n_clicks")],
#     [State("container", "children")],
# )
# def display_graphs(n_clicks, div_children):

#     new_child = html.Div(
#         style={
#             "width": "45%",
#             "display": "inline-block",
#             "outline": "thin lightgrey solid",
#             "padding": 10,
#         },
#         children=[
#             dcc.Dropdown(id={"type": "xVariable", "index": n_clicks}, value=None),
#             dcc.Dropdown(
#                 id={"type": "yVariable", "index": n_clicks}, value=None, multi=True
#             ),
#             html.Button(
#                 "Update", id={"type": "updateButton", "index": n_clicks}, n_clicks=0
#             ),
#             dcc.Graph(
#                 id={"type": "graph", "index": n_clicks},
#             ),
#         ],
#     )
#     div_children.append(new_child)
#     return div_children


# @callback(ServersideOutput("store", "data"), Trigger("btn", "n_clicks"), memoize=True)
# def query_data(self):
#     time.sleep(1)
#     df = mongoconfig.loadSingleDataset(
#         "project 1",
#         "incheon",
#         "none",
#         [
#             "ts",
#             "700FIC028_Y",
#             "700II781C_Y",
#             "700II782C_Y",
#             "700II783C_Y",
#             "700LI770B_Y",
#         ],
#     )
#     df = pd.json_normalize(df)
#     return df

#     # return


# # Dropdown
# @callback(
#     Output({"type": "xVariable", "index": MATCH}, "options"), Input("store_eda", "data")
# )
# def update_x_dropdown(df):
#     print(df)
#     return [{"label": column, "value": column} for column in df]


# @callback(
#     Output({"type": "yVariable", "index": MATCH}, "options"), Input("store_eda", "data")
# )
# def update_y_dropdown(df):
#     return [{"label": column, "value": df.columns.get_loc(column)} for column in df]


# # Update Graph
# @callback(
#     Output({"type": "graph", "index": MATCH}, "figure"),
#     [
#         Input("store", "data"),
#         Input({"type": "updateButton", "index": MATCH}, "n_clicks"),
#         State({"type": "xVariable", "index": MATCH}, "value"),
#         State({"type": "yVariable", "index": MATCH}, "value"),
#     ],
# )
# def update_graph(df, n_clicks, xValue, yValue):
#     if n_clicks is 0:
#         raise PreventUpdate

#     fig = px.line(df, x=xValue, y=df.columns[yValue], title="Incheon Data")
#     print(n_clicks)
#     return fig


###########################################################################
import time
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Output, Input
from dash_extensions.enrich import Dash, Trigger, ServersideOutput

app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div(
    [
        html.Button("Query data", id="btn"),
        dcc.Dropdown(id="dd"),
        dcc.Graph(id="graph"),
        dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot"),
    ]
)
