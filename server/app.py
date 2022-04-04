#Make a simple rest api

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
    guilds = db.relationship('Guild', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
# Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    message = db.Column(db.String(120))
    time = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))



# Role model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')
    guild_id = db.Column(db.Integer)
    permissions = db.Column(db.Integer)

# Channel model
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    messages = db.relationship('Message', backref='channel', lazy='dynamic')
    guild_id = db.Column(db.Integer)
    permissions = db.Column(db.Integer)

#Guild Model
class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    owner_id = db.Column(db.Integer)
    channels = db.relationship('Channel', backref='guild', lazy='dynamic')
    users = db.relationship('User', backref='guild', lazy='dynamic')
    roles = db.relationship('Role', backref='guild', lazy='dynamic')


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'guilds', 'role_id')



# Message Schema
class MessageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'message', 'user_id', 'time', 'author', 'guild_id', 'channel_id')

# Channel Schema
class ChannelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'messages', 'guild_id', 'permissions')

# Role Schema
class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'users', 'guild_id', 'permissions')

# Guild Schema
class GuildSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'owner_id', 'channels', 'users', 'roles')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

channel_schema = ChannelSchema()
channels_schema = ChannelSchema(many=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

guild_schema = GuildSchema()
guilds_schema = GuildSchema(many=True)

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
# Create a guild
@app.route('/guild', methods=['POST'])
def add_guild():
    name = request.json['name']
    description = request.json['description']
    owner_id = request.json['owner_id']
    token = request.json['token']
    if token == secret_key:
        new_guild = Guild(name=name, owner_id=owner_id, description=description)
        db.session.add(new_guild)
        db.session.commit()
        return guild_schema.jsonify(new_guild)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Get all users in a guild
@app.route('/guild/<int:guild_id>/users', methods=['GET'])
def get_users_in_guild(guild_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        users = guild.users
        result = users_schema.dump(users)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Delete a guild
@app.route('/guild/<int:guild_id>', methods=['DELETE'])
def delete_guild(guild_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        db.session.delete(guild)
        db.session.commit()
        return jsonify({"message": "Guild deleted"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Get all guilds
@app.route('/guilds', methods=['GET'])
def get_guilds():
    token = request.json['token']
    if token == secret_key:
        all_guilds = Guild.query.all()
        result = guilds_schema.dump(all_guilds)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Create a channel
@app.route('/guild/<int:guild_id>/channel', methods=['POST'])
def add_channel(guild_id):
    name = request.json['name']
    guild_id = guild_id
    token = request.json['token']
    if token == secret_key:
        new_channel = Channel(name=name, guild_id=guild_id)
        db.session.add(new_channel)
        db.session.commit()
        return channel_schema.jsonify(new_channel)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Get all channels in a guild
@app.route('/guild/<int:guild_id>/channels', methods=['GET'])
def get_channels_in_guild(guild_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        channels = guild.channels
        result = channels_schema.dump(channels)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a channel from a guild
@app.route('/guild/<int:guild_id>/channel/<int:channel_id>', methods=['GET'])
def get_channel_from_guild(guild_id, channel_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        channel = Channel.query.get(channel_id)
        result = channel_schema.dump(channel)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

    
# Delete a channel
@app.route('/guild/<int:guild_id>/channel/<int:channel_id>', methods=['DELETE'])
def delete_channel(guild_id, channel_id):
    token = request.json['token']
    if token == secret_key:
        channel = Channel.query.get(channel_id)
        db.session.delete(channel)
        db.session.commit()
        return jsonify({"message": "Channel deleted"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Create a role
@app.route('/guild/<int:guild_id>/role', methods=['POST'])
def add_role(guild_id):
    name = request.json['name']
    guild_id = guild_id
    token = request.json['token']
    permissions = request.json['permissions']
    if token == secret_key:
        new_role = Role(name=name, guild_id=guild_id, permissions=permissions)
        db.session.add(new_role)
        db.session.commit()
        return role_schema.jsonify(new_role)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Assign a role to a user
@app.route('/guild/<int:guild_id>/user/<int:user_id>/role/<int:role_id>', methods=['POST'])
def assign_role(guild_id, user_id, role_id):
    token = request.json['token']
    if token == secret_key:
        user = User.query.get(user_id)
        role = Role.query.get(role_id)
        user.roles.append(role)
        db.session.commit()
        return jsonify({"message": "Role assigned"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Get a role from guild
@app.route('/guild/<int:guild_id>/role/<int:role_id>', methods=['GET'])
def get_role_from_guild(guild_id, role_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        role = Role.query.get(role_id)
        result = role_schema.dump(role)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Get all roles in a guild
@app.route('/guild/<int:guild_id>/roles', methods=['GET'])
def get_roles_in_guild(guild_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        roles = guild.roles
        result = roles_schema.dump(roles)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Delete a role
@app.route('/guild/<int:guild_id>/role/<int:role_id>', methods=['DELETE'])
def delete_role(guild_id, role_id):
    token = request.json['token']
    if token == secret_key:
        role = Role.query.get(role_id)
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Join a guild
@app.route('/guild/<int:guild_id>/join', methods=['POST'])
def join_guild(guild_id):
    token = request.json['token']
    user_id = request.json['user_id']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        user = User.query.get(user_id)
        guild.users.append(user)
        db.session.commit()
        return jsonify({"message": "Joined guild"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Leave a guild
@app.route('/guild/<int:guild_id>/leave', methods=['POST'])
def leave_guild(guild_id):
    token = request.json['token']
    user_id = request.json['user_id']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        user = User.query.get(user_id)
        guild.users.remove(user)
        db.session.commit()
        return jsonify({"message": "Left guild"})
    if token != secret_key:
        return jsonify({"message": "Invalid token"})
# Kick a user from a guild
@app.route('/guild/<int:guild_id>/kick/<int:user_id>', methods=['POST'])
def kick_user(guild_id, user_id):
    token = request.json['token']
    if token == secret_key:
        guild = Guild.query.get(guild_id)
        user = User.query.get(user_id)
        guild.users.remove(user)
        db.session.commit()
        return jsonify({"message": "User kicked"})
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
@app.route('/useremail/<email>', methods=['GET'])
def get_user_by_email(email):
    token = request.json['token']
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

# Get last 10 messages from a channel
@app.route('/guild/<int:guild_id>/channel/<int:channel_id>/messages', methods=['GET'])
def get_messages(guild_id, channel_id):
    token = request.json['token']
    if token == secret_key:
        channel = Channel.query.get(channel_id)
        messages = channel.messages
        result = messages_schema.dump(messages)
        return jsonify(result)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})

# Add a message to a channel
@app.route('/guild/<int:guild_id>/channel/<int:channel_id>/message', methods=['POST'])
def add_message(guild_id, channel_id):
    token = request.json['token']
    content = request.json['content']
    if token == secret_key:
        channel = Channel.query.get(channel_id)
        user = User.query.get(request.json['user_id'])
        new_message = Message(content=content, channel=channel, user=user)
        db.session.add(new_message)
        db.session.commit()
        return message_schema.jsonify(new_message)
    if token != secret_key:
        return jsonify({"message": "Invalid token"})


# Get a message by id from a channel
@app.route('/guild/<int:guild_id>/channel/<int:channel_id>/message/<int:message_id>', methods=['GET'])
def get_message(guild_id, channel_id, message_id):
    token = request.json['token']
    if token == secret_key:
        channel = Channel.query.get(channel_id)
        message = Message.query.get(message_id)
        result = message_schema.dump(message)
        return jsonify(result)
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