from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import mongoconfig
import pandas as pd

# modeling
from modelingAlgorithm import Algorithm

import os
import sys

sys.path.append("./modeling")

Modeling = Namespace("modeling")


@Modeling.route("/<algorithm>")
class modeling(Resource):
    def post(self, algorithm):
        """Algorithm wrapping"""
        modelingAlgorithm = getattr(Algorithm, algorithm)

        """Get Request Parameter"""
        projectName = request.get_json()["projectName"]
        modelingDataset = request.get_json()["modelingDataset"]
        modelingRequest = request.get_json()["modelingRequest"]
        splitRatio = request.get_json()["splitRatio"]

        """ Practice """
        # projectName = "project 1"
        # modelingDataset = {"draft": "draft1", "grid": 0}

        """Get Draft Info"""
        draft = mongoconfig.loadDraft(projectName)
        gridID = str(modelingDataset)

        filterModel = {}
        renameModel = []
        typeModel = []
        fillNaModel = {}
        deleteModel = []
        deleteNaModel = []

        if gridID in draft["filterModel"]:
            filterModel = draft["filterModel"][gridID]
        if gridID in draft["datasetToLoad"]:
            tableName = draft["datasetToLoad"][gridID]
        if gridID in draft["columnModel"]:
            columnModel = draft["columnModel"][gridID][tableName]
        if gridID in draft["renameModel"]:
            renameModel = draft["renameModel"][gridID]
        if gridID in draft["typeModel"]:
            typeModel = draft["typeModel"][gridID]
        if gridID in draft["fillNaModel"]:
            fillNaModel = draft["fillNaModel"][gridID]
        if gridID in draft["deleteModel"]:
            deleteModel = draft["deleteModel"][gridID]
        if gridID in draft["deleteNaModel"]:
            deleteNaModel = draft["deleteNaModel"][gridID]

        data = mongoconfig.loadSingleDataset(
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

        df = pd.json_normalize(data)

        """ debug """
        # print(modelingRequest)
        # print("splitRatio", splitRatio)
        # print("modelingRequest", modelingRequest)

        """ modeling """
        return modelingAlgorithm(df, splitRatio, modelingRequest)
