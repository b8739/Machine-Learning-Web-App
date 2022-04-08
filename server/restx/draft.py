from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import mongoconfig

Draft = Namespace("draft")


@Draft.route("")
class loadDraft(Resource):
    def get(self):
        projectName = request.args.get("projectName")
        try:
            draftInfo = mongoconfig.loadDraft(projectName)
            return jsonify(draftInfo)
        except Exception as e:
            return jsonify(str(e)), 500
