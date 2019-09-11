from flask import Flask,request,jsonify
from todo.config import DevConfig

from flask_sqlalchemy import SQLAlchemy

#CONFIG
app=Flask(__name__)
app.config.from_object(DevConfig)


#INIT DB
db=SQLAlchemy(app)

from todo import routes

