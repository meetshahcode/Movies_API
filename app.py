import string
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float ,ARRAY
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_manager,jwt_required,create_access_token,create_refresh_token

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'movies.db')
app.config["JWT_SECRET_KEY"] = 'unique_key'

SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

"""
use flask db_create command in terminal
"""
@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database Created !!")

"""
use flask db_drop command in terminal
"""
@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("database Dropped !!")
@app.cli.command("db_seed")
def db_seed():

    pass


"""
Defining ORM model
"""

"""
API
"""
@app.route("/movie_details/<int:movie_id>",methods=["GET","POST"])
def movie_details(movie_id):
    movie = movie.query.filter_by(movie_id=movie_id).first()
    if movie:
        result = movie_schema.dump(movie)
        return jsonify(result)
    else:
        return jsonify(message = "The movie id does not exist."),404

"""
for movies
"""
class Movies(db.Model):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key = True)
    movie_title  = Column(String,nullable = False)
    movie_year = Column(Integer,nullable = False)
    movie_rating = Column(Float,nullable = False)
    movie_genres = Column(ARRAY(String),nullable = False)

class movieSchema(ma.Schema):
    class Meta:
        fields = ("movie_id","movie_title","movie_year","movie_rating","movie_genres")

movie_schema = movieSchema()
movies_schema = movieSchema(many = True)