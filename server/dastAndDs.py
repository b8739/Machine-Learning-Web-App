## 사용안하고 있어서 여기 보관
# # Dash
# dash_app1 = Dash(__name__, server=application, url_base_pathname="/dashapp1/")
# # --------------------------------------------------------------------------------------------------------

# # boston
# # data = mongoconfig.loadSingleDataset("project 1", "data_0", "none", ["CRIM", "ZN"])
# # df = pd.json_normalize(data)
# # print(df)
# # columns = df.head().columns

# # iris
# df_original = iris()
# # df_original = iris()[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
# # df = pd.concat(
# #     [df_original + np.random.randn(*df_original.shape) * 0.1 for i in range(10000)]
# # )
# # print(len(df))
# columns = df_original.head().columns

# # reset 버튼도 만들어두기
# # mongoDB로 dataset의 정보가 변경될때마다 x,y 컬럼의 정보도 변경을 해야 함
# dash_app1.layout = html.Div(
#     [
#         html.Br(),
#         html.H2("EDA %d Rows" % len(df_original)),
#         html.Br(),
#         dcc.Dropdown(
#             id="dataset",
#             options=[{"label": x, "value": x} for x in ["180mb", "boston"]],
#             clearable=False,
#             placeholder="Choose Dataset",
#             value=None,
#         ),
#         dcc.Dropdown(
#             id="xVariable",
#             options=[{"label": x, "value": x} for x in ["CRIM", "ZN"]],
#             clearable=False,
#             placeholder="X Axis",
#             value=None,
#         ),
#         dcc.Dropdown(
#             id="yVariable",
#             options=[{"label": x, "value": x} for x in ["CRIM", "ZN"]],
#             # options=[{"label": x, "value": x} for x in df_original.head().columns[1:]],
#             clearable=False,
#             placeholder="Y Axis",
#             value=None,
#         ),
#         # Graph
#         dcc.Graph(id="edaChart"),
#         html.Div(id="dropdown-container", children=[]),
#         html.Br(),
#         # dash_table.DataTable(
#         #     id="df-stack-table",
#         #     columns=[{"name": i, "id": i} for i in df.head().columns],
#         #     data=df.head(15).to_dict("records"),
#         # ),
#     ]
# )

# fig = px.scatter()
# # print(fig)


# @dash_app1.callback(
#     # Output("edaChart", "figure"),
#     Output("dropdown-container", "children"),
#     Input("dataset", "value"),
#     Input("xVariable", "value"),
#     Input("yVariable", "value"),
#     State("dropdown-container", "children"),
# )
# def updateData(dataset, xVariable, yVariable, children):
#     if dataset != None and xVariable != None or yVariable != None:
#         # fig = px.scatter()
#         # else:
#         #     print("load")
#         # data = mongoconfig.loadSingleDataset(
#         #     "project 1", "boston", "none", ["CRIM", "ZN"]
#         # )
#         # df = pd.json_normalize(data)
#         #     fig = px.scatter(df, x=xVariable, y=yVariable)
#         pts = hv.Scatter(df_original, kdims=["sepal_length"], vdims=["sepal_width"])
#         scatter = datashade(pts).opts(title="Datashader with %d points" % len(pts))
#         components = to_dash(dash_app1, [scatter], reset_button=True)
#         children.append(components.children)
#         print("this is layout", dash_app1)
#     return children

#####################################################################################


###########################################################################
# edaApp = Dash(
#     __name__,
#     plugins=[dl.plugins.pages],
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     prevent_initial_callbacks=True,
#     server=application,
#     url_base_pathname="/edaApp/",
# )
# edaApp.config["suppress_callback_exceptions"] = True

# for x in dash.page_registry.values():
#     print(x)

# navbar = dbc.NavbarSimple(
#     dbc.DropdownMenu(
#         [
#             dbc.DropdownMenuItem(page["name"], href=page["path"])
#             for page in dash.page_registry.values()
#             if page["module"] != "pages.not_found_404"
#         ],
#         nav=True,
#         label="More Pages",
#     ),
#     brand="Multi Page App Plugin Demo",
#     color="primary",
#     dark=True,
#     className="mb-2",
# )

# edaApp.layout = dbc.Container(
#     [
#         navbar,
#         dl.plugins.page_container,
#         html.Button("Query data (edaapp)", id="btn"),
#         dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot"),
#     ],
#     fluid=True,
# )


# @edaApp.callback(
#     ServersideOutput("store", "data"), Trigger("btn", "n_clicks"), memoize=True
# )
# def query_data():
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
