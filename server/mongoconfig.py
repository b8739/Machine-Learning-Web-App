from flask import Flask, jsonify
from flask_pymongo import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from bson import json_util
from bson.code import Code
import json
import pandas as pd
from collections import OrderedDict
from dataSummarizer import summarizeData
from distributionData import getDistributionData
import time


# atlas
# client = pymongo.MongoClient(
#     "mongodb+srv://jaeho:0000@cluster0.a71en.mongodb.net/atticDatabase?retryWrites=true&w=majority"
# )

# atlas starbucks
client = pymongo.MongoClient(
    "mongodb://jaeho:0000@cluster0-shard-00-00.a71en.mongodb.net:27017,cluster0-shard-00-01.a71en.mongodb.net:27017,cluster0-shard-00-02.a71en.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-ut0ooq-shard-0&authSource=admin&retryWrites=true&w=majority"
)

# local shell
# client = pymongo.MongoClient("mongodb://localhost:27017/atticDatabase", 27017)

# aws ec2 shell
# client = pymongo.MongoClient("mongodb://jaeho:0000@3.35.85.176/atticDatabase", 27017)

db = client.atticDatabase
datasetCollection = pymongo.collection.Collection(db, "datasetCollection")
infoCollection = pymongo.collection.Collection(db, "infoCollection")
modelingCollection = pymongo.collection.Collection(db, "modelingCollection")
draftCollection = pymongo.collection.Collection(db, "draftCollection")
statisticsCollection = pymongo.collection.Collection(db, "statisticsCollection")
distCollection = pymongo.collection.Collection(db, "distCollection")

coll_dataset = db["datasetCollection"]
coll_info = db["infoCollection"]
coll_modeling = db["modelingCollection"]
coll_draft = db["draftCollection"]
coll_stats = db["statisticsCollection"]
coll_dist = db["distCollection"]

""" Data Upload """


def parse_json(data):
    return json_util.dumps(data, sort_keys=False)


def mongoimport(projectName, tableName, data):
    """RESET"""
    # emptyCollection()

    # db & collection 정의
    # data =  pd.read_csv('/Users/jeongjaeho/attic_project/testcode/concrete.csv')

    """ 1) infoCollection: Project/Table Info """
    diff = time.time()
    project_id = ObjectId()
    datasetID = ObjectId()

    fields = list(data.columns)

    infoDict = {}
    infoDict["projects"] = [
        {
            "id": project_id,
            "name": projectName,
            "datasets": [{"id": datasetID, "name": tableName, "fields": fields}],
        }
    ]
    coll_info.insert(infoDict)
    print("infoDict inserted", time.time() - diff)

    """ 2) datasetCollection: Dataset """
    # json 변환
    diff = time.time()
    # payload = data.to_dict("records")  # dict
    payload = json.loads(data.to_json(orient="records"))  # json
    print("loades json", time.time() - diff)

    diff = time.time()
    for item in payload:
        item.update({"projectID": project_id, "datasetID": datasetID})
    coll_dataset.create_index([("datasetID", 1)])
    print("create dataset index", time.time() - diff)
    diff = time.time()
    try:
        # coll_dataset.insert(payload, {"ordered": True})
        coll_dataset.insert_many(payload, ordered=False)
    except Exception as e:
        errorMessage = "An exception occurred ::", str(e)
        coll_info.delete({"datasets": [{"id": datasetID}]})
        return errorMessage
    print("insert into db", time.time() - diff)

    diff = time.time()
    insertStatistics(project_id, datasetID, data)
    print("calculate statistics + insert into db", time.time() - diff)
    # insertDistribution(project_id, datasetID, data)

    return "Data Successfully Uploaded To DB"


""" Data Remove """


def deleteDataset(projectName, tableName):
    ID = getID(projectName, tableName)
    coll_info.delete_many(
        {
            "projects.id": ID["projectID"],
            "projects.datasets.id": ID["datasetID"],
        }
    )
    coll_dataset.delete_many(
        {
            "projectID": ID["projectID"],
            "datasetID": ID["datasetID"],
        }
    )
    coll_stats.delete_many(
        {
            "projectID": ID["projectID"],
            "datasetID": ID["datasetID"],
        }
    )
    coll_dist.delete_many(
        {
            "projectID": ID["projectID"],
            "datasetID": ID["datasetID"],
        }
    )
    coll_draft.delete_many({})

    return


def emptyCollection():
    coll_info.delete_many({})
    coll_dataset.delete_many({})
    coll_modeling.delete_many({})
    coll_stats.delete_many({})
    coll_draft.delete_many({})
    return


""" Count """


def countDocs(projectName, tableName):
    """1) QUERY projectID and datasetID filter by projectName, tableName"""

    ID = getID(projectName, tableName)

    """ 2) QUERY dataset docs filter by projectID, datasetID """
    result = coll_dataset.find(
        {"projectID": ID["projectID"], "datasetID": ID["datasetID"]}
    ).count()
    print(result)
    return result


""" Load Table/Column Info"""


def getAllTables(projectName):
    queryResult = coll_info.aggregate(
        [
            {
                "$match": {
                    "projects.name": projectName,
                },
            },
            {"$project": {"_id": 0, "projects.datasets.name": 1}},
        ]
    )

    tableList = []
    for v in list(queryResult):
        tableList.append(v["projects"][0]["datasets"][0]["name"])

    return tableList


def getAllColumns(projectName, tableName):
    if isinstance(tableName, list) == True:
        return
    else:
        queryResult = coll_info.aggregate(
            [
                {
                    "$match": {
                        "projects.name": projectName,
                        "projects.datasets.name": tableName,
                    },
                },
                {"$project": {"_id": 0, "fields": "$projects.datasets.fields"}},
            ]
        )

        columns = list(queryResult)[0]["fields"][0][0]
    return columns


""" Distribution"""


def insertDistribution(project_id, datasetID, data):
    distData = getDistributionData(data)
    payload = json.loads(distData)
    print(payload)
    payload.update({"projectID": project_id, "datasetID": datasetID})
    coll_dist.create_index([("datasetID", 1)])
    coll_dist.insert(payload)
    return "Distributino inserted"


""" Statistics  """


def insertStatistics(project_id, datasetID, data):
    statistics = summarizeData(data)
    payload = json.loads(statistics)
    payload.update({"projectID": project_id, "datasetID": datasetID})
    coll_stats.create_index([("datasetID", 1)])
    coll_stats.insert(payload)
    return


def getStatisticValue(ID, featureName, statisticType):
    result = list(
        coll_stats.aggregate(
            [
                {
                    "$match": {
                        "datasetID": ID["datasetID"],
                    }
                },
                {"$replaceRoot": {"newRoot": "$" + featureName}},
                {"$project": {"_id": 0, statisticType: 1}},
            ]
        )
    )
    value = result[0][statisticType]
    return value


def loadStatistics(projectName, tableName):
    ID = getID(projectName, tableName)

    result = list(
        coll_stats.aggregate(
            [
                {"$match": {"datasetID": ID["datasetID"]}},
                {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},
            ]
        )
    )
    return result


""" Data Type """


def getDataTypes(
    projectName, tableName, columnModel
):  # projectName, tableName, columnModel
    # projectName = "project 1"
    # tableName = "boston"
    # columnModel = ["CRIM", "ZN", "CHAS"]

    ID = getID(projectName, tableName)

    # 1. Set Match Model
    matchModel = {
        "projectID": ID["projectID"],
        "datasetID": ID["datasetID"],
    }
    matchModel.update({"ID": 1})

    # 2. Set Projection Model
    projectModel = {}
    for column in columnModel:
        projectModel.update({column: {"$type": "$" + column}})

    # Query
    result = list(
        coll_dataset.aggregate(
            [
                {"$match": matchModel},
                # {"$limit": 1},
                # {
                #     "$group": {
                #         "_id": {"$type": "$CRIM"},
                #         # "datatype": {"$type": "$CRIM"},
                #     },
                # },
                {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},  # 제외할 컬럼
                {"$project": projectModel},
            ]
        )
    )
    print(result[0])
    return result[0]


""" Get ID """


def getID(projectName, tableName):
    result = coll_info.find_one(
        {"projects.name": projectName, "projects.datasets.name": tableName},
        {"_id": 0, "projects.id": 1, "projects.datasets.id": 1},
    )

    projectID = result["projects"][0]["id"]
    datasetID = result["projects"][0]["datasets"][0]["id"]

    ID = {"projectID": projectID, "datasetID": datasetID}

    return ID


""" Edit Rows """


def updateRows(projectName, tableName, updateTransaction):
    ID = getID(projectName, tableName)
    for v in updateTransaction:
        print(v)
        coll_dataset.update_one(
            {
                "$and": [
                    {"projectID": ID["projectID"]},
                    {"datasetID": ID["datasetID"]},
                    {"ID": v["ID"]},
                ]
            },
            {"$set": {v["field"]: v["newValue"]}},
        )
    return "dd"


def deleteRows(projectName, tableName, rowIDs):
    ID = getID(projectName, tableName)
    for i in rowIDs:
        print(i)
        coll_dataset.delete_one(
            {
                "$and": [
                    {"projectID": ID["projectID"]},
                    {"datasetID": ID["datasetID"]},
                    {"ID": i},
                ]
            }
        )
    return "dd"


""" Load Infinite Row Model"""


def loadSingleDataset(
    projectName,
    tableName,
    filterModel="none",
    columnModel=[],
    renameModel=[],
    typeModel=[],
    fillNaModel={},
    deleteNaModel={},
    deleteModel=[],
    graphSelectModel=[],
    startRow="none",
    limitNum="none",
):
    # 1) Get ID Dataset Name
    ID = getID(projectName, tableName)
    matchModel = {
        "projectID": ID["projectID"],
        "datasetID": ID["datasetID"],
    }
    # 2) Set Match Model (Filter)

    if filterModel != "none":
        for i in filterModel:
            matchModel.update(i)
    # 2) Set Delete Model (Filter)

    if deleteModel != []:
        matchModel.update({"ID": {"$nin": deleteModel}})
    if graphSelectModel != []:
        matchModel.update({"ID": {"$in": graphSelectModel}})
    # 3) Set Projection Model (Display, Re-name)

    projectionModel = {}

    # 3-1 Set Projection Model (Display)
    if columnModel:
        for column in columnModel:
            projectionModel.update({column: 1})
        projectionModel.update({"ID": 1})

    # 3-2 Set Projection Model (Data Type)
    if typeModel:
        for value in typeModel:
            projectionModel.update(value)

    # 3-2 Set Projection Model (FillNA)
    if fillNaModel:
        for key, value in fillNaModel.items():
            if value == 0 or value == 1:
                projectionModel.update({key: {"$ifNull": ["$" + key, value]}})
            else:
                statisticValue = getStatisticValue(ID, key, value)
                projectionModel.update({key: {"$ifNull": ["$" + key, statisticValue]}})

    # 3-2 Set Projection Model (Delete NA)
    if deleteNaModel:
        for key, value in deleteNaModel.items():
            if value == True:
                matchModel.update({key: {"$ne": None}})

    # 3-3 Set Projection Model (Re-name)

    for value in renameModel:
        projectionModel.update({value["to"]: "$" + value["from"]})

    pipeline = [{"$match": matchModel}]

    if startRow != "none":
        pipeline.append({"$skip": startRow})
    if limitNum != "none":
        pipeline.append({"$limit": limitNum})
    pipeline.append({"$project": {"_id": 0, "datasetID": 0, "projectID": 0}})
    pipeline.append({"$project": projectionModel})

    # 5 Query

    rows = list(coll_dataset.aggregate(pipeline))

    return rows


def loadMergedDataset(
    projectName,
    tableName,
    startRow,
    endRow,
    filterModel=[],
    columnsToAdd=[],
    renameModel=[],
    typeModel={},
    deleteModel=[],
):
    # 1. Get ID (datasetName, projectName)
    ID = {}
    for index, table in enumerate(tableName):
        ID[index] = getID(projectName, table)

    # 2. Set Match Model (1st Match: datasetName, skip, limit)

    matchModel = {
        "$and": [
            # Dataset 선별
            {"$or": []},
            # 구간 선별
            {"ID": {"$gte": startRow, "$lt": endRow}},
        ]
    }

    for key, value in ID.items():
        matchModel["$and"][0]["$or"].append({"datasetID": value["datasetID"]})

    # 3 Set Filter model (2nd Match: nin, gte, lt, etc...)
    finalFilterModel = {}

    if filterModel != "none":
        for i in filterModel:
            finalFilterModel.update(i)

    # 4. Set Column Model ($group, push)
    columns = []
    for index, tableName in enumerate(tableName):
        for key, value in enumerate(columnsToAdd[tableName]):
            columns.append(value)

    columnModel = {}

    for value in columns:
        columnModel[value] = "$" + value

    # 2. Set Merge Model
    mergeModel = {"$mergeObjects": []}
    for key, value in columnModel.items():
        mergeModel["$mergeObjects"].append(
            {key: {"$arrayElemAt": ["$columns." + key, 0]}}
        )
    # 3. Set Project Model
    projectModel = {}

    for value in columns:
        projection = {value: "$columns." + value}
        projectModel.update(projection)

    projectModel.update({"ID": "$_id"})

    # 4. Query
    result = list(
        coll_dataset.aggregate(
            [
                {"$match": matchModel},  # 아직 document가 분리되어 있기 때문에 여기에 filter를 넣을 수 없음
                {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},  # 제외할 컬럼
                {
                    "$group": {
                        "_id": "$ID",
                        "columns": {"$push": columnModel},
                    }
                },
                {
                    "$group": {
                        "_id": "$_id",
                        "columns": {"$push": mergeModel},
                    }
                },
                {"$unwind": "$columns"},
                {"$sort": {"_id": 1}},
                {"$project": projectModel},  # 컬럼 이름 바꾸기 (ex. columns.CRIM -> CRIM)
                {"$match": finalFilterModel},
                {"$project": {"_id": 0}},
            ]
        )
    )
    # print("filterModel", filterModel)

    return result


""" Load Whole Data """


def getAllDataSingle(projectName, tableName, filterModel=[]):
    """RETURN"""

    ID = getID(projectName, tableName)

    matchModel = {
        "projectID": ID["projectID"],
        "datasetID": ID["datasetID"],
    }
    if filterModel != "none":
        for i in filterModel:
            matchModel.update(i)

    result = list(
        coll_dataset.aggregate(
            [
                {"$match": matchModel},
                {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},
            ]
        )
    )
    df = pd.json_normalize(result)
    # parsedResult = parse_json(result)
    # print(df)
    return df


def getAllDataMulti(projectName, tableName, columnModel, filterModel=[]):

    # 1. Get ID (datasetName, projectName)
    ID = {}
    for index, table in enumerate(tableName):
        ID[index] = getID(projectName, table)

    matchModel = {}

    result = {}
    df = {}
    dfToMerge = []
    if filterModel != "none":
        for i in filterModel:
            matchModel.update(i)
    # set column model
    projectionModel = []
    for index, tableName in enumerate(tableName):
        print(index)
        projectionModel.append({})
        for key, value in enumerate(columnModel[tableName]):
            projectionModel[index].update({value: 1})

    # Query Multiple Times
    for key, value in ID.items():
        result[key] = list(
            coll_dataset.aggregate(
                [
                    {"$match": matchModel},
                    {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},
                    {"$project": projectionModel[key]},
                ]
            )
        )
        df[key] = pd.json_normalize(result[key])
        dfToMerge.append(df[key])

    finalResult = pd.concat(dfToMerge, axis=1)

    print(finalResult)

    # parsedResult = parse_json(result)
    # print(df)
    return finalResult


""" Load Graph Data """


def getSingleFieldData(projectName, tableName, fieldName):
    """RETURN"""

    ID = getID(projectName, tableName)

    result = list(
        coll_dataset.aggregate(
            [
                {
                    "$match": {
                        "projectID": ID["projectID"],
                        "datasetID": ID["datasetID"],
                    }
                },
                {"$project": {"_id": 0, fieldName: 1}},
            ]
        )
    )
    df = pd.json_normalize(result)
    # parsedResult = parse_json(result)
    # print(df)
    return df


def getSampleData(projectName, tableName, sampleSize):

    ID = getID(projectName, tableName)

    result = list(
        coll_dataset.aggregate(
            [
                {
                    "$match": {
                        "projectID": ID["projectID"],
                        "datasetID": ID["datasetID"],
                    }
                },
                {"$sample": {"size": sampleSize}},
                {"$project": {"_id": 0, "projectID": 0, "datasetID": 0}},
            ]
        )
    )
    df = pd.json_normalize(result)
    return df


""" Draft """


def saveDraft(
    projectName,
    filterModel,
    gridList,
    deleteModel,
    datasetToLoad,
    columnModel,
    columnState,
    renameModel,
    typeModel,
    fillNaModel,
    clientFilterModel,
    deleteNaModel,
    gridType,
):
    # 현재는 upsert시에 draftName을 기준으로 사용하는데 더 좋은 unique value가 있는지 찾아보자

    finalDocument = {
        "projectName": projectName,
        "filterModel": filterModel,
        "clientFilterModel": clientFilterModel,
        "gridList": gridList,
        "deleteModel": deleteModel,
        "datasetToLoad": datasetToLoad,
        "columnModel": columnModel,
        "columnState": columnState,
        "renameModel": renameModel,
        "typeModel": typeModel,
        "fillNaModel": fillNaModel,
        "deleteNaModel": deleteNaModel,
        "gridType": gridType,
    }

    coll_draft.create_index([("ID", 1)])
    coll_draft.update({"projectName": projectName}, finalDocument, True)

    return "Draft Saved"


def loadDraft(projectName):
    draftInfo = list(
        coll_draft.aggregate(
            [
                {
                    "$match": {"projectName": projectName},
                },
                {"$project": {"_id": 0, "projectName": 0}},
            ]
        )
    )
    if draftInfo:
        draftInfo[0]["filterModel"] = json.loads(draftInfo[0]["filterModel"])
        draftInfo[0]["typeModel"] = json.loads(draftInfo[0]["typeModel"])
        return draftInfo[0]
    else:
        return []


def loadDraftList():
    queryResult = list(
        coll_draft.aggregate(
            [
                {
                    "$match": {},
                },
                {"$project": {"_id": 0, "draftName": 1}},
            ]
        )
    )
    # queryResult = coll_draft.find()
    return queryResult


""" Modeling """


def saveModel(modelInfo):
    coll_modeling.update({"projectName": modelInfo["projectName"]}, modelInfo, True)

    return "Saved Successfully"


def getAllCases(projectName):

    queryResult = list(
        coll_modeling.aggregate(
            [
                {
                    "$match": {
                        "projectName": projectName,
                    },
                },
                {"$project": {"_id": 0, "case_name": 1, "algorithm": 1}},
            ]
        )
    )

    return queryResult


def loadModelCase(modelName):
    result = list(
        coll_modeling.aggregate(
            [
                {
                    "$match": {
                        "case_name": modelName,
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        # "modelingSummary": 1,
                        # "graphSources": 1,
                    }
                },
            ]
        )
    )

    return result[0]


""" Practice """


def test1():
    ID = getID("project 1", "cnull2")

    matchModel = {
        "projectID": ID["projectID"],
        "datasetID": ID["datasetID"],
    }

    result = coll_dataset.aggregate(
        [
            {"$match": matchModel},
            {"$skip": 0},  # Lazy Loading
            {"$limit": 0},  # Lazy Loading
            {"$project": {"projectID": 0, "datasetID": 0}},
        ]
    )
    print(list(result))
    return


def mapReducePractice():
    projectName = "project 1"
    tableName = "boston"

    ID = getID(projectName, tableName)

    mapCode = Code(
        "function () {"
        "  this.CRIM.forEach(function(z) {"
        "    emit(z, 1);"
        "  });"
        "}"
    )
    reduceCode = Code("function (crimValue, one) {" "return Array.sum(crimValue);" "}")

    matchModel = {
        "projectID": ID["projectID"],
        "datasetID": ID["datasetID"],
    }

    result = coll_dataset.map_reduce(mapCode, reduceCode, "myresults")

    for doc in result.find():
        print(doc)
    return jsonify("s")
