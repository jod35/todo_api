from flask import request,jsonify,make_response
from todo import app,db
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from todo.models import User,Todo
import jwt
from datetime import datetime

#routes
@app.route('/user',methods=['GET'])
def get_all_users():
   #this query returns all the users from the database

   users=User.query.all()
   
   if not users:
       return jsonify({"message":"There are no users!"})
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
    
#get one specific user
@app.route('/user/<int:id>',methods=['GET'])
def get_one_user(id):
   user=User.query.get(id)
   if not user:
       return jsonify({"message": "User doesnot exist"})
   output=[]
   user_data={}
   user_data['public_id']=user.public_id
   user_data['name']=user.name
   user_data['password']=user.password
   user_data['admin']=user.admin
   #we then add the dictionaries to our output lists
   output.append(user_data)

   return jsonify({"user":output})

#create a user
@app.route('/user', methods=['POST'])
def create_user():
    data= request.get_json()
    hashed_password=generate_password_hash(data['password'],method='sha256')
    new_user=User(public_id=str(uuid.uuid4()),name=data['name'],password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"New User Added Successfully"})

#change a user to an admin
@app.route('/user/<int:id>', methods=['PUT'])
def promote_user(id):
    user=User.query.get(id)
    if not user:
        return jsonify({"message":"User does not exist"})
    user.admin=True
    db.session.commit()
    return jsonify({"message ":"User has changed to an admin!"})

#delete a specific user
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user=User.query.get(id)

    if not user:
        return jsonify({"message":"User Does Not Exist"})
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"User Deleted Successfully"})

#create some security in form of JWT authentication
@app.route('/login')
def login_user():
   auth=request.authorization
    
   #if no creadentials are supplied to the API, it should throw a login required message 
   if not auth or not auth.username or auth.password:
       return make_response('Could not verify',401,{"WWW-Authenticate":"Basic realm = 'Login required'"})
   
   user=User.query.filter_by(name=auth.username).first()
   
   
   if not user:
       return make_response('Could not verify',401,{"WWW-Authenticate":"Basic realm = 'Login required'"})

   if check_password_hash(user.password,auth.password):
       token=jwt.encode({'public_id': user.public_id,'exp':datetime.utcnow()+ datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])

       return jsonify({"token": token.decode('UTF-8')})
   
   return make_response('Could not verify',401,{"WWW-Authenticate":"Basic realm = 'Login required'"})