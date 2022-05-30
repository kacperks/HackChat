# this is a python restful api with flask and sqlite3 Authentication: Bearer Token

import datetime
import os
import uuid
import configparser
from functools import wraps
import jwt # PYJWT
from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
global rankid 
# Ranks:
# 1. Admin
# 2. Mod
# 3. User
# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SECRET_KEY'] = 'This is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = app.config['SECRET_KEY']
# Initialize Database
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)

# User Class/Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    rankid = db.Column(db.Integer)


# Message Class/Model
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    message = db.Column(db.String(5000))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorated
def rank_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        if current_user.rankid <= rankid:
            return jsonify({'message': 'You do not have the required rank'})
        return f(current_user, *args, **kwargs)

    return decorated

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'password', 'rankid')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
# Message Schema
class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author', 'message')

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

# Register a new user
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        public_id = str(uuid.uuid4())
        name = request.json['name']
        password = request.json['password']
        rankid = 3
        # check if user already exists
        user = Users.query.filter_by(name=name).first()
        if not user:
            new_user = Users(public_id=public_id, name=name, password=password, rankid=rankid)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'New user created successfully'})
        else:
            return jsonify({'message': 'User already exists'})
# Login a user
@app.route('/login', methods=['GET', 'POST'])
def login():
    name = request.json['name']
    password = request.json['password']
    if name == '' or password == '':
        return jsonify({'message': 'name or password is missing', 'code': 400})
    user = Users.query.filter_by(name=name).first()
    if user is None:
        return jsonify({'message': 'User does not exist', 'code': 404})
    if user.password == password:
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)
        return jsonify({'token': token, 'code': 200})
    return jsonify({'message': 'Wrong password', 'code': 401})
# Get User info
@app.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    # remove password from response
    user = Users.query.filter_by(public_id=current_user.public_id).first()
    #remove password from response
    user.password = None
    user.public_id = None
    return user_schema.jsonify(user)
    
# Grant rank to user
rankid = 1
@app.route('/grant_rank', methods=['POST'])
@rank_required
def grant_rank(current_user):
    if request.method == 'POST':
        userid = request.json['userid']
        rankid = request.json['rankid']
        if userid == '' or rankid == '':
            return jsonify({'message': 'userid or rankid is missing', 'code': 400})
        user = Users.query.filter_by(public_id=userid).first()
        if user is None:
            return jsonify({'message': 'User does not exist', 'code': 404})
        user.rankid = rankid
        db.session.commit()
        return jsonify({'message': 'Rank granted successfully', 'code': 200})
# Revoke rank from user
rankid = 1
@app.route('/revoke_rank', methods=['POST'])
@rank_required
def revoke_rank(current_user):
    if request.method == 'POST':
        userid = request.json['userid']
        if userid == '':
            return jsonify({'message': 'userid is missing', 'code': 400})
        user = Users.query.filter_by(public_id=userid).first()
        if user is None:
            return jsonify({'message': 'User does not exist', 'code': 404})
        user.rankid = 0
        db.session.commit()
        return jsonify({'message': 'Rank revoked successfully', 'code': 200})

# Get all users
rankid = 1
@app.route('/users', methods=['GET'])
@rank_required
def get_users(current_user):
    users = Users.query.all()
    return jsonify({'users': users_schema.dump(users), 'code': 200})

# Get user by id
@app.route('/user/<id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, id):
    # remove password from response
    user = Users.query.filter_by(id=id).first()
    if user is None:
        return jsonify({'message': 'User does not exist', 'code': 404})
    return jsonify({'user': user_schema.dump(user), 'code': 200})

# Get User by name
@app.route('/user/name/<name>', methods=['GET'])
@token_required
def get_user_by_name(current_user, name):
    # remove password from response
    user = Users.query.filter_by(name=name).first()
    if user is None:
        return jsonify({'message': 'User does not exist', 'code': 404})
    return jsonify({'user': user_schema.dump(user), 'code': 200})

# Get last 10 messages
@app.route('/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    messages = Messages.query.order_by(Messages.id.desc()).limit(10).all()
    return jsonify({'messages': messages_schema.dump(messages), 'code': 200})
# Get a single message
@app.route('/message/<id>', methods=['GET'])
@token_required
def get_message(id):
    message = Messages.query.get(id)
    if message is None:
        return jsonify({'message': 'Message not found', 'code': 404})
    result = message_schema.dump(message)
    return jsonify(result, 200)

# Change Password
@app.route('/change_password', methods=['POST'])
@token_required
def change_password(test):
    oldpassword = request.json['oldpassword']
    newpassword = request.json['newpassword']
    if oldpassword == '' or newpassword == '':
        return jsonify({'message': 'name or password is missing', 'code': 400})
    user = Users.query.filter_by(public_id=test.public_id).first()
    if user is None:
        return jsonify({'message': 'User does not exist', 'code': 404})
    if user.password != oldpassword:
        return jsonify({'message': 'Wrong password', 'code': 409})
    user.password = newpassword
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'})

# Change Name
@app.route('/change_name', methods=['POST'])
@token_required
def change_name(current_user):
    if request.method == 'POST':
        name = request.json['name']
        if name == '':
            return jsonify({'message': 'Name is missing', 'code': 400})
        current_user.name = name
        db.session.commit()
        return jsonify({'message': 'Name changed successfully', 'code': 200})

# Add a new message
@app.route('/add_message', methods=['POST'])
@token_required
def add_message(current_user):
    if request.method == 'POST':
        author = current_user.name
        message = request.json['message']
        if message == '':
            return jsonify({'message': 'Message is missing', 'code': 400})
        new_message = Messages(author=author, message=message)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message added successfully', 'code': 200})

# Delete a message
rankid = 2
@app.route('/delete_message/<id>', methods=['DELETE'])
@rank_required
def delete_message(id, current_user):
    message = Messages.query.get(id)
    if message is None:
        return jsonify({'message': 'Message not found', 'code': 404})
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully', 'code': 200})

# Delete Specific User
rankid = 1
@app.route('/delete_user/<id>', methods=['DELETE'])
@rank_required
def delete_user(id, current_user):
    user = Users.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found', 'code': 404})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully', 'code': 200})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)