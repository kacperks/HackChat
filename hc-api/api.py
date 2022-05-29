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
    admin = db.Column(db.Boolean)

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
def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, secret_key)
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            if current_user.admin is False:
                return jsonify({'message': 'Restricted area you must be admin'})
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'password', 'admin')

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
        name = request.json['name']
        password = request.json['password']
        public_id = str(uuid.uuid4())
        admin = False
        if name == '' or password == '':
            return jsonify({'message': 'name or password is missing', 'code': 400})
        if Users.query.filter_by(name=name).first() is not None:
            return jsonify({'message': 'User already exists', 'code': 409})
        user = Users(name=name, password=password, public_id=public_id, admin=admin)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully','code':200})

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

# Get all users
@app.route('/users', methods=['GET'])
@admin_required
def get_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result, 200)

# Get last 10 messages
@app.route('/messages', methods=['GET'])
@token_required
def get_messages(test):
    all_messages = Messages.query.order_by(Messages.id.desc()).limit(10).all()
    result = messages_schema.dump(all_messages)
    return jsonify(result, 200)

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
@app.route('/delete_message/<id>', methods=['DELETE'])
@admin_required
def delete_message(current_user, id):
    if request.method == 'DELETE':
        message = Messages.query.get(id)
        if message is None:
            return jsonify({'message': 'Message not found', 'code': 404})
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully', 'code': 200})

# Delete Specific User
@app.route('/delete_user/<id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, id):
    if request.method == 'DELETE':
        user = Users.query.get(id)
        if user is None:
            return jsonify({'message': 'User not found', 'code': 404})
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully', 'code': 200})

# Delete Specific Message
@app.route('/delete_specific_message/<id>', methods=['DELETE'])
@admin_required
def delete_specific_message(current_user, id):
    if request.method == 'DELETE':
        message = Messages.query.get(id)
        if message is None:
            return jsonify({'message': 'Message not found', 'code': 404})
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully', 'code': 200})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)