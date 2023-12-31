from flask import jsonify, request, send_file
from flask_restful import Resource

from datetime import datetime
import os

import models
import sqlite


class UserH(Resource):
    def get(self, id: int):
        return jsonify(sqlite.get_user(id).serialize())


class PackageH(Resource):
    def get(self, id: int):
        return jsonify(sqlite.get_package(id).serialize())


class ReleaseH(Resource):
    def get(self, package_name: str, version: str):
        return jsonify(sqlite.get_release(package_name, version).serialize())


class InstallPackageH(Resource):
    def post(self, package_name: str, version: str):
        if version == "max":
            version = sqlite.get_last_release(package_name)
            if isinstance(version, models.Error):
                return jsonify(version)
            version = version.version
        return send_file(f"/packages/{package_name}/release-{version}.zip", as_attachment=True)


class AddReleaseH(Resource):
    def post(self):
        if 'file' not in request.files:
            return models.Error(400, "No file provided")
        data = request.get_json()
        if "author" not in data:
            return jsonify(models.Error(400, "Can't Auth your account")), 400
        if "id" not in data["author"] or "password" not in data["author"]:
            return jsonify(models.Error(400, "Can't Auth your account")), 400
        if not sqlite.check_auth(data["author"]["id"], data["author"]["password"]):
            return jsonify(models.Error(400, "Can't Auth your account")), 400
        if not sqlite.get_package(data["name"]):
            os.makedirs(data["name"])
            sqlite.add_package(data["name"], data["author"]["id"], data["github_url"], data["avatar"])
        elif data["author"]["id"] != sqlite.get_package(data["name"]).author_id:
            return jsonify(models.Error(400, "Can't change package")), 400
        if sqlite.get_release(data["name"], data["version"]):
            return jsonify(models.Error(400, "Release version already exists")), 400
        try:
            if len(tuple(map(int, data["version"].split('.')))) != 3:
                return jsonify(models.Error(400, "Wrong version format use `x.x.x`")), 400
        except Exception:
            return jsonify(models.Error(400, "Wrong version format use `x.x.x`")), 400
        sqlite.add_release(data["name"], data["version"], data["author"]["id"], data["description"], int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
        file = request.files["file"]
        file.save(f"/packages/{data['name']}/release-{data['version']}.zip")
        return jsonify(models.Error(200, "")), 200

