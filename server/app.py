from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow_sqlalchemy
import os
import API
import configparser
from functools import wraps
import time as times

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


parser = configparser.ConfigParser()
parser.read('config.ini')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


secret_key = parser.get('SECURITY', 'SECRET_KEY')
db = SQLAlchemy(app)
ma = Marshmallow(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

# Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    message = db.Column(db.String(120))
    time = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Message Schema
class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'message', 'user_id', 'time', 'author')

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


@app.route('/' ,methods=['GET'])
def index():
    return 'Api documentiation link: https://documenter.getpostman.com/view/16377775/UVyrTFxg' 

# Register a user
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    token = request.json['token']
    if token == secret_key:
        new_user = User(username=username, email=email, password=password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    token = request.json['token']
    if token == secret_key:
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a user by id
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    token = request.json['token']
    if token == secret_key:
        user = User.query.get(id)
        return user_schema.jsonify(user)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a user by username
@app.route('/usernick/<username>', methods=['GET'])
def get_user_by_username(username):
    token = request.json['token']
    if token == secret_key:
        user = User.query.filter_by(username=username).first()
        return user_schema.jsonify(user)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a user by email
@app.route('/useremail/<token>/<email>', methods=['GET'])
def get_user_by_email(token,email):
    if token == secret_key:
        user = User.query.filter_by(email=email).first()
        return user_schema.jsonify(user)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Remove a user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    token = request.json['token']
    if token == secret_key:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return user_schema.jsonify(user)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get last 10 messages
@app.route('/messages', methods=['GET'])
def get_messages():
    all_messages = Message.query.order_by(Message.time.desc()).limit(10).all()
    result = messages_schema.dump(all_messages)
    return jsonify(result)

# Add a message
@app.route('/message', methods=['POST'])
def add_message():
    token = request.json['token']
    if token == secret_key:
        message = request.json['message']
        user_id = request.json['user_id']
        time = times.time()
        author = API.get_user_by_id(user_id)['username']
        new_message = Message(message=message, user_id=user_id, time=time, author=author)

        db.session.add(new_message)
        db.session.commit()

        return user_schema.jsonify(new_message)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a message by id
@app.route('/message/<id>', methods=['GET'])

def get_message(id):
    token = request.json['token']
    if token == secret_key:
        message = Message.query.get(id)
        return message_schema.jsonify(message)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Remove a message by id
@app.route('/message/<id>', methods=['DELETE'])
def delete_message(id):
    token = request.json['token']
    if token == secret_key:
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return message_schema.jsonify(message)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})



#run the app
if __name__ == '__main__':
    app.run(debug=True)
