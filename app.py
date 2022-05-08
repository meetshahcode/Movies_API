from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_manager,jwt_required,create_access_token,create_refresh_token
from flask_mail import Mail,Message

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'movies.db')
app.config["JWT_SECRET_KEY"] = 'unique_key'

SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)
