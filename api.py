from flask import Flask,request,jsonify
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
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
   #this query returns all the users from the database

   users=User.query.all()

   output=[]
   #since sqlachemy results cannot be returned directly as json, we make our own json objects from the results.

   for user in users:
       user_data={}

       user_data['public_id']=user.public_id
       user_data['name']=user.name
       user_data['password']=user.password
       user_data['admin']=user.admin
       #we then add the dictionaries to our output lists
       output.append(user_data)

   return jsonify({"users":output})
    
@app.route('/user/<user_id>',methods=['GET'])
def get_one_user():
   return ''

@app.route('/user', methods=['POST'])
def create_user():
    data= request.get_json()
    hashed_password=generate_password_hash(data['password'],method='sha256')
    new_user=User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"New User Added Successfully"})

@app.route('/user/<user_id>', methods=['PUT'])
def promote_user():
    return ''

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''

if __name__ == "__main__":
    app.run(debug=True)