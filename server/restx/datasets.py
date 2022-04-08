from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import mongoconfig

# pyarrow
import pyarrow as pa
from pyarrow import csv

Datasets = Namespace("datasets")


@Datasets.route("")
class dataupload(Resource):
    # data upload
    def post(self):
        # Route for our Processing and Details Page
        if request.method == "POST" and "csv_data" in request.files:
            tableName = request.args.get("tableName")
            projectName = request.args.get("projectName")
            file = request.files["csv_data"]

            # pyarrow
            pyarrow_table = csv.read_csv(file)
            try:
                df = pyarrow_table.to_pandas()

            except ValueError as e:
                return jsonify(str(e))
            empColumn = [col for col in df.columns if col == ""]
            if empColumn:
                return jsonify(
                    "Please get rid of empty field name in the dataset before upload"
                )
            # df = df.dropna(axis=0)
            df = df.reset_index().rename(columns={"index": "ID"})

            result = mongoconfig.mongoimport(projectName, tableName, df)

        # return summarizeData(df)
        return jsonify(result)


@Datasets.route("/<tableName>")
class AggDataset(Resource):
    def post(self, tableName):
        projectName = request.get_json()["projectName"]
        startRow = request.get_json()["startRow"]
        endRow = request.get_json()["endRow"]
        filterModel = request.get_json()["filterModel"]
        columnModel = request.get_json()["columnModel"]
        renameModel = request.get_json()["renameModel"]
        typeModel = request.get_json()["typeModel"]
        fillNaModel = request.get_json()["fillNaModel"]
        deleteNaModel = request.get_json()["deleteNaModel"]
        deleteModel = request.get_json()["deleteModel"]
        graphSelectModel = request.get_json()["graphSelectModel"]
        gridType = request.get_json()["gridType"]
        limitNum = int(endRow) - int(startRow)

        # print("columnModel", columnModel)

        if gridType == "AgGridSingle":
            try:
                rows = mongoconfig.loadSingleDataset(
                    projectName,
                    tableName,
                    filterModel,
                    columnModel,
                    renameModel,
                    typeModel,
                    fillNaModel,
                    deleteNaModel,
                    deleteModel,
                    graphSelectModel,
                    startRow,
                    limitNum,
                )
                return jsonify(rows)
            except Exception as e:
                return jsonify(str(e)), 500
        # multiple
        else:
            try:
                rows = mongoconfig.loadMergedDataset(
                    projectName,
                    tableName,
                    startRow,
                    endRow,
                    filterModel,
                    columnModel,
                    renameModel,
                    typeModel,
                    deleteModel
                    # typeModel
                )
                return jsonify(rows)

            except Exception as e:
                return jsonify(str(e)), 500
