import requests
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float ,ARRAY
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'movies.db')
app.config["JWT_SECRET_KEY"] = 'unique_key'

SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

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



def getdatafromOMDAPI(title = None,year = None,imdbId = None):
    url = r"https://www.omdbapi.com/?apikey=6e0a855e"

    if title and title != "":
        url = url + f"&t={title}"
    if year:
        url = url + f"&y={year}"
    if imdbId and imdbId != "":
        url = url + f"&i={imdbId}"
    response = (requests.get(url=url)).json()
    if response["Response"]  == "False" or response["Response"] == False : return False
    Rating = 0.0
    Year = 0
    try:
        Rating = float(response["imdbRating"] ) 
    except:
        Rating =  0.0
    try:
        Year = int(response["Year"])
    except:
        Year = 0
    movie = Movies(
            movie_imdbID = response["imdbID"],
            movie_genres = response["Genre"],
            movie_title= response["Title"],
            movie_year = Year,
            movie_rating = Rating
    )
    db.session.add(movie)
    db.session.commit()
    return True
"""
API
"""
@app.route("/")
def hello():
    return jsonify(message = "Welcome to movie api."),200


@app.route("/movie_by_id/<int:movie_id>",methods=["GET"])
def movie_by_id(movie_id):
    movie = Movies.query.filter_by(movie_id=movie_id).first()
    if movie:
        result = movie_schema.dump(movie)
        return jsonify(result)
    else:
        return jsonify(message = "The movie id does not exist."),404


@app.route("/movie_by_imdbid/<string:movie_imdbID>",methods=["GET"])
def movie_by_imdbid(movie_imdbID):
    movie = Movies.query.filter(Movies.movie_imdbID.contains(movie_imdbID)).first()
    if movie:
        result = movie_schema.dump(movie)
        return jsonify(result)
    elif getdatafromOMDAPI(imdbId=movie_imdbID):
        movie = Movies.query.filter(Movies.movie_imdbID.contains(movie_imdbID)).first()
        result = movie_schema.dump(movie)
        return jsonify(result)
    else:
        return jsonify(message = "The movie id does not exist."),404


@app.route("/movie_by_title/<string:movie_title>",methods=["GET"])
def movie_by_title(movie_title):
    movies = Movies.query.filter(Movies.movie_title.contains(movie_title))
    if movies.count()>0:
        result = movies_schema.dump(movies)
        return jsonify(result)
    elif getdatafromOMDAPI(movie_title):
        movies = Movies.query.filter(Movies.movie_title.contains(movie_title))
        result = movies_schema.dump(movies)
        return jsonify(result)
    else:
        return jsonify(message = "The movie with the title does not exist."),404


@app.route("/movie_by_year/<int:year>",methods=["GET"])
def movie_by_year(year):
    movies = Movies.query.filter_by(movie_year=year)
    if movies.count()>0:
        result = movies_schema.dump(movies)
        return jsonify(result)
    else:
        return jsonify(message = "The movie with given year does not exist."),404

@app.route("/movie_by_rating/<float:movie_rating>",methods = ["GET"])
def movie_by_rating(movie_rating):
    movies = Movies.query.filter(Movies.movie_rating >= movie_rating )
    if movies.count()>0:
        result = movies_schema.dump(movies)
        return jsonify(result)
    else:
        return jsonify(message = "The movie with the genres does not exist."),404

@app.route("/movie_by_genres/<string:movie_genres>",methods=["GET"])
def movie_by_genres(movie_genres):
    movielist = [i.strip() for i in movie_genres.split(",")]
    genres = ",%".join(sorted(movielist))
    movies = Movies.query.filter(Movies.movie_genres.contains(genres))
    if movies.count()>0:
        result = movies_schema.dump(movies)
        return jsonify(result)
    else:
        return jsonify(message = "The movie with the genres does not exist."),404



"""
Defining ORM model
"""
"""
for movies
"""

class Movies(db.Model):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key = True)
    movie_title  = Column(String,nullable = False)
    movie_year = Column(Integer,nullable = False)
    movie_rating = Column(Float,nullable = False)
    movie_genres = Column(String,nullable = False)
    movie_imdbID = Column(String,unique = True)


class movieSchema(ma.Schema):
    class Meta:
        fields = ("movie_id","movie_title","movie_year","movie_rating","movie_genres","movie_imdbID")


movie_schema = movieSchema()
movies_schema = movieSchema(many = True)