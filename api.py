from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#CONFIG
app=Flask(__name__)
app.secret_key='3ddab6977d5f660c'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///api.db'

#INIT DB
db=SQLAlchemy(app)

#DATABASE TABLES

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    public_id=db.Column(db.String(),unique=True)
    name=db.Column(db.String(80))
    password=db.Column(db.String(80))
    admin=db.Column(db.Boolean())

class Todo(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    text=db.Column(db.String(255))
    complete=db.Column(db.Boolean)
    user_id=db.Column(db.Integer())

#routes
@app.route('/user',methods=['GET'])
def get_all_users():
   return ''
    
@app.route('/user/<user_id>',methods=['GET'])
def get_one_user():
   return ''

@app.route('/user', methods=['POST'])
def create_user():
    return ''

@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''

if __name__ == "__main__":
    app.run(debug=True)