from flask import Flask, request, redirect, url_for, session
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import socket
import json
from werkzeug.security import generate_password_hash, check_password_hash
import os, sys
sys.path.append(os.getcwd())
import registration_model as registrationModel
import app_configuration as appConf

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

class DBConnection(Resource):
    def get(self):
        return registrationModel.getDbConnection()

api.add_resource(DBConnection,"/getDbConnection")

if __name__ == '__main__': 
    app.run()