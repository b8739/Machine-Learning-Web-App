import sys
import os

sys.path.append("./modeling")
sys.path.append("./simulation")
sys.path.append("./schema")
sys.path.append("./restx")

# flask
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    request,
    url_for,
    Response,
    send_from_directory,
    send_file,
    make_response,
    Markup,
)


from flask_restx import Resource, Api
from jinja2 import Template

from flask_cors import CORS


from flask_uploads import UploadSet, configure_uploads, IMAGES, DATA, ALL


# db config
from config import *
import time

# from werkzeug import secure_filename

# from werkzeug.utils import secure_filename


import mongoconfig

# import dynamoconfig


import datetime
import time
import json

# EDA Packages
import pandas as pd
import numpy as np

# summarizer
# from dataSummarizer import summarizeData
# from distributionData import getDistributionData
# from newDataSummarizer import test
from normalDistribution import randGenerator_nd


# simulation
from simulation import getSimulationResult

# pyarrow
import pyarrow as pa
from pyarrow import csv

# collections
from collections import OrderedDict, defaultdict

# configuration
DEBUG = True

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "dist")
STATIC_URL_PATH = os.path.join(STATIC_PATH, "static")

# instantiate the app

application = Flask(
    __name__, static_folder=STATIC_PATH, static_url_path="", template_folder=STATIC_PATH
)
application.config.from_object(__name__)
application.config["TEMPLATES_AUTO_RELOAD"] = False

# enable CORS
CORS(application, resources={r"/*": {"origins": "*"}})

# restx
from datasets import Datasets
from modeling import Modeling
from draft import Draft


api = Api(application)
api.add_namespace(Datasets, "/datasets")
api.add_namespace(Modeling, "/modeling")
api.add_namespace(Draft, "/draft")


# route
@application.route("/", defaults={"path": ""})
@application.route("/<string:path>")
def index(path):
    # return render_template('index.html')
    # return application.send_static_file('index.html')
    return send_from_directory(STATIC_PATH, "index.html")


@application.route("/test")
class test:
    def get():
        print("hi")
        return jsonify("get test")


@application.route("/loadStatistics", methods=["POST"])
def loadStatistics():

    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]

    result = mongoconfig.loadStatistics(projectName, tableName)
    return jsonify(result[0])


@application.route("/loadProjects", methods=["GET"])
def loadProjects():
    dd = ["sampleProject"]
    return jsonify(dd)


@application.route("/showTables", methods=["POST"])
def showTables():
    projectName = request.get_json()["projectName"]
    try:
        tableList = mongoconfig.getAllTables(projectName)
        return jsonify(tableList)
    except Exception as e:
        return jsonify(str(e)), 500


@application.route("/loadColumns", methods=["GET", "POST"])
def loadColumns():
    tableName = request.get_json()["tableName"]
    projectName = request.get_json()["projectName"]
    try:
        columnList = mongoconfig.getAllColumns(projectName, tableName)
        return jsonify(columnList)
    except Exception as e:
        return jsonify(str(e)), 500


@application.route("/loadDraftList", methods=["GET", "POST"])
def loadDraftList():
    draftList = mongoconfig.loadDraftList()
    return jsonify(draftList)


@application.route("/loadDatasetSize", methods=["GET", "POST"])
def loadDatasetSize():
    tableName = request.get_json()["tableName"]
    projectName = request.get_json()["projectName"]
    print(tableName)
    print(projectName)

    docsCount = mongoconfig.countDocs(projectName, tableName)

    return jsonify(docsCount)


@application.route("/loadEditGraphData", methods=["POST"])
def loadEditGraphData():

    """바뀐 버전"""
    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]
    filterModel = request.get_json()["filterModel"]
    columnModel = request.get_json()["columnModel"]
    renameModel = request.get_json()["renameModel"]
    typeModel = request.get_json()["typeModel"]
    fillNaModel = request.get_json()["fillNaModel"]
    deleteNaModel = request.get_json()["deleteNaModel"]
    deleteModel = request.get_json()["deleteModel"]
    gridType = request.get_json()["gridType"]

    result = mongoconfig.loadSingleDataset(
        projectName,
        tableName,
        filterModel,
        columnModel,
        renameModel,
        typeModel,
        fillNaModel,
        deleteNaModel,
        deleteModel,
    )
    # 꼭 json.normalize 해야하는지 (메모리) 검토 필요

    result = pd.json_normalize(result)
    print(result)
    # 컬럼 하나만 가져와야 되는데 무조건 ID가 끼어있으므로 제거 (단 ID 컬럼을 로드하는 경우에는 삭제하지 않기 위해 if문)
    if len(result.columns) > 1:
        result = result.drop("ID", axis=1)

    result = result.fillna("null")  # nan을 null값으로 처리안해주면 apex에서 인식못함

    return json.dumps(result.to_dict(orient="list", into=OrderedDict))


@application.route("/loadFeatureGraphData", methods=["POST"])
def loadFeatureGraphData():
    # feature 이름 받아서 변수로 저장
    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]
    datasetSize = request.get_json()["datasetSize"]
    # a) df 사이즈가 1000보다 작은 데이터
    if datasetSize < 1000:
        sample = mongoconfig.getAllDataSingle(projectName, tableName)
        return json.dumps(sample.to_dict(orient="list", into=OrderedDict))

    # b) df 사이즈가 1000보다 큰 데이터
    else:
        sampleSize = datasetSize * 0.1
        randomSample = mongoconfig.getSampleData(projectName, tableName, sampleSize)
    return json.dumps(randomSample.to_dict(orient="list", into=OrderedDict))


@application.route("/exportAllData", methods=["POST"])  # mongoDB
def exportAllData():
    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]
    filterModel = request.get_json()["filterModel"]
    gridType = request.get_json()["gridType"]
    columnModel = request.get_json()["columnModel"]
    renameModel = request.get_json()["renameModel"]
    typeModel = request.get_json()["typeModel"]
    fillNaModel = request.get_json()["fillNaModel"]
    deleteNaModel = request.get_json()["deleteNaModel"]
    deleteModel = request.get_json()["deleteModel"]
    print(gridType)
    if gridType == "AgGridSingle":
        result = mongoconfig.loadSingleDataset(
            projectName,
            tableName,
            filterModel,
            columnModel,
            renameModel,
            typeModel,
            fillNaModel,
            deleteNaModel,
            deleteModel,
        )
    # elif gridType == "AgGridMultiple":
    #     result = mongoconfig.getAllDataMulti(
    #         projectName, tableName, columnModel, filterModel
    #     )
    df = pd.json_normalize(result)
    print(df)

    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
    # return Response(
    #     result,
    #     mimetype="text/csv",
    #     content_type="application/octet-stream",
    #     headers={"Content-disposition": "attachment; filename=myplot.csv"},
    # )
    # return send_file(
    #     result,
    #     mimetype="text/csv",
    #     attachment_filename="downloaded_file_name.csv",  # 다운받아지는 파일 이름.
    #     as_attachment=True,
    # )


@application.route("/updateRows", methods=["POST"])  # mongoDB
def updateRows():
    tableName = request.get_json()["tableName"]
    projectName = request.get_json()["projectName"]
    updateTransaction = request.get_json()["updateTransaction"]
    result = mongoconfig.updateRows(projectName, tableName, updateTransaction)
    return result


@application.route("/deleteRows", methods=["POST"])  # mongoDB
def deleteRows():
    tableName = request.get_json()["tableName"]
    projectName = request.get_json()["projectName"]
    selectedIDs = request.get_json()["selectedIDs"]
    print(selectedIDs)
    result = mongoconfig.deleteRows(projectName, tableName, selectedIDs)
    return result


""" 
addData: Dataset에 data를 'Add'할 때 라우팅
"""


@application.route("/loadGroupingData", methods=["POST"])
def loadGroupingData():
    # Session = sessionmaker(bind=dataset_schema.engine,autocommit=False)
    Session = scoped_session(sessionmaker(bind=dataset_schema.engine, autocommit=False))
    session = Session()

    tableName = request.get_json()["tableName"]
    groupingFeature = request.get_json()["groupingFeature"]
    otherFeatures = request.get_json()["otherFeatures"]

    allFeatures = []
    allFeatures.append(groupingFeature)

    for key in otherFeatures:
        allFeatures.append(key)
    print(allFeatures)

    df = pd.read_sql_table(tableName, session.bind, columns=allFeatures)

    groupLength = len(df[groupingFeature].unique())

    # numeric 이거나 category의 unique값이 5개를 넘어갈 때, 5개로 설정
    if groupLength > 5:
        groupLength = 5

    # print(df)
    groupedResult = []
    for key in otherFeatures:
        groupedResult.append(
            df.groupby(
                pd.cut(df[groupingFeature], groupLength, right=False).astype(str)
            )[key].apply(list)
        )

    result = pd.DataFrame(groupedResult).to_dict(orient="list", into=OrderedDict)

    session.commit()
    session.close()
    # .to_dict(orient='list',into=OrderedDict)
    return json.dumps(result)


""" 
loadData: Frontend에서 Dataset을 로드해오는 라우팅
"""


""" 
infinite-loading Test: 
"""


@application.route("/saveDraft", methods=["POST"])
def saveDraft():
    try:
        projectName = request.get_json()["projectName"]
        filterModel = request.get_json()["filterModel"]
        gridList = request.get_json()["gridList"]
        deleteModel = request.get_json()["deleteModel"]
        datasetToLoad = request.get_json()["datasetToLoad"]
        columnModel = request.get_json()["columnModel"]
        columnState = request.get_json()["columnState"]
        renameModel = request.get_json()["renameModel"]
        typeModel = request.get_json()["typeModel"]
        fillNaModel = request.get_json()["fillNaModel"]
        deleteNaModel = request.get_json()["deleteNaModel"]
        clientFilterModel = request.get_json()["clientFilterModel"]
        gridType = request.get_json()["gridType"]

        result = mongoconfig.saveDraft(
            projectName,
            json.dumps(filterModel),
            gridList,
            deleteModel,
            datasetToLoad,
            columnModel,
            columnState,
            renameModel,
            json.dumps(typeModel),
            fillNaModel,
            clientFilterModel,
            deleteNaModel,
            gridType,
        )

        # columnsToExclude는 dataset마다 넣어야하는 컬럼을 담고 있는 object of array 가 와야 함
        return jsonify(result)
    except Exception as e:
        return jsonify(str(e)), 500


@application.route("/getDataTypes", methods=["POST"])
def getDataTypes():

    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]
    columnModel = request.get_json()["columnModel"]

    result = mongoconfig.getDataTypes(
        projectName,
        tableName,
        columnModel,
    )

    return jsonify(result)


@application.route("/dropTable", methods=["POST"])
def dropTable():
    projectName = request.get_json()["projectName"]
    tableName = request.get_json()["tableName"]
    mongoconfig.deleteDataset(projectName, tableName)
    return jsonify("dropTable")


def sqlDataMapper(pythonDtype):
    if pythonDtype == "int16":
        return "smallint"
    if pythonDtype == "int32":
        return "integer"
    if pythonDtype == "int64":
        return "bigint"
    if pythonDtype == "float32":
        return "real"
    if pythonDtype == "float64":
        return "FLOAT"
    if pythonDtype == "string":
        return "BINARY"
    if pythonDtype == "datatime64":
        return "DATE"


@application.route("/loadRandomInfo", methods=["GET"])
def loadRandomInfo():
    tableName = request.args.get("tableName")
    Session = scoped_session(sessionmaker(bind=dataset_schema.engine, autocommit=False))
    session = Session()

    df = pd.read_sql_table(tableName, session.bind)
    df = df.fillna(np.nan)
    del df["ID"]
    return randGenerator_nd(df)


@application.route("/saveModelCase", methods=["POST"])
def saveModelCase():
    # POST REQUEST
    projectName = request.get_json()["projectName"]
    modelingDataset = request.get_json()["modelingDataset"]
    splitRatio = request.get_json()["splitRatio"]

    case_name = request.get_json()["case_name"]
    algorithm = request.get_json()["algorithm"]

    inputs = request.get_json()["inputs"]
    targets = request.get_json()["targets"]

    parameters = request.get_json()["parameters"]

    graphSources = request.get_json()["graphSources"]
    modelingSummary = request.get_json()["modelingSummary"]

    canvasState = request.get_json()["canvasState"]

    final = {
        "projectName": projectName,
        "modelingDataset": modelingDataset,
        "splitRatio": splitRatio,
        "case_name": case_name,
        "algorithm": algorithm,
        "inputs": inputs,
        "targets": targets,
        "parameters": parameters,
        "graphSources": graphSources,
        "modelingSummary": modelingSummary,
        "canvasState": canvasState,
    }
    result = mongoconfig.saveModel(final)
    # print("case_name", case_name)
    # print("algorithm", algorithm)
    # print("inputs", inputs)
    # print("targets", targets)
    # print("parameters", parameters)
    return jsonify(result)


@application.route("/saveCanvas", methods=["GET"])
def saveCanvas():
    projectName = request.get_json()["projectName"]
    state = request.get_json()["state"]
    result = mongoconfig.saveCanvas(projectName, state)

    return jsonify(result)


@application.route("/loadCases", methods=["GET"])
def loadCases():
    cases = mongoconfig.getAllCases("project 1")
    print(cases)
    return jsonify(cases)


@application.route("/getCaseFeatures", methods=["POST"])
def getCaseFeatures():
    Session = scoped_session(sessionmaker(bind=model_schema.engine, autocommit=False))
    session = Session()
    # caseID = request.get_json()['caseID']
    caseID = request.get_json()["caseID"]

    inputRows = (
        session.query(dataset_schema.Input)
        .filter(dataset_schema.Input.cases_id == caseID)
        .all()
    )
    targetRows = (
        session.query(dataset_schema.Target)
        .filter(dataset_schema.Target.cases_id == caseID)
        .all()
    )

    inputs = []
    targets = []

    for row in inputRows:
        inputs.append(row.name)

    for row in targetRows:
        targets.append(row.name)

    session.commit()
    session.close()
    return jsonify({"inputs": inputs, "targets": targets})


@application.route("/loadModelCase", methods=["POST"])
def loadModelCase():
    caseName = request.get_json()["caseName"]
    result = mongoconfig.loadModelCase(caseName)
    return result


@application.route("/runSimulation", methods=["POST"])
def runSimulation():
    Session = scoped_session(sessionmaker(bind=dataset_schema.engine, autocommit=False))
    session = Session()

    df = pd.read_sql_table("dataset", session.bind)
    df = df.fillna(np.nan)
    del df["ID"]
    # from front-end
    observedVariable = request.get_json()["observedVariable"]
    rangeInfo = request.get_json()["rangeInfo"]
    target = request.get_json()["target"]
    print(rangeInfo)
    session.commit()
    session.close()
    return getSimulationResult(df, observedVariable, target, rangeInfo)


if __name__ == "__main__":
    application.run(port=8000)  # host="0.0.0.0" 외부접속
