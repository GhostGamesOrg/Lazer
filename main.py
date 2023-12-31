from flask import Flask, jsonify, request
from flask_restful import Api

import models
import sqlite
from handlers import UserH, PackageH, ReleaseH, AddReleaseH, InstallPackageH

sqlite.create_tables()
app = Flask(__name__)
api = Api(app)

api.add_resource(UserH, '/user/<int:id>')
api.add_resource(PackageH, '/package/<int:id>')
api.add_resource(ReleaseH, '/release/<string:package_name>/<string:version>')

api.add_resource(InstallPackageH, '/install/release/<string:package_name>/<string:version>')
api.add_resource(AddReleaseH, '/create/release')

sqlite.add_user(
    _id=sqlite.add_auth("1234567890"),
    name="Test",
    avatar="None",
    description="Test user",
    github_url="https://github.com/Animemchik"
)
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6969, debug=True)
