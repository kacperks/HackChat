
import re
import requests
import json
import configparser
# make a config file

parser = configparser.ConfigParser()
parser.read('config.ini')
token = parser.get('SECURITY', 'SECRET_KEY')

# Request the data from the server
def register(username, email, password):
    url = "http://localhost:5000/user"
    payload = json.dumps({
        "username": username,
        "email": email,
        "password": password,
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return response.json()
def get_users():
    url = "http://localhost:5000/users"
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
def get_user_by_id(id):
    if id == str:
        pass
    else:
        id = str(id)
    url = "http://localhost:5000/user/" + id
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
def get_user_by_username(username):
    url = "http://localhost:5000/usernick/" + username
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()


def get_user_by_email(email):
    url = "http://localhost:5000/useremail/" + email
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
def delete_user(id):
    if id == str:
        pass
    else:
        id = str(id)
    url = "http://localhost:5000/user/" + id
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers, data = payload)
    return response.json()

def add_message(message, user_id, time):
    if user_id == str:
        pass
    else:
        user_id = str(user_id)
    url = "http://localhost:5000/message"
    payload = json.dumps({
        "message": message,
        "user_id": user_id,
        "time": time,
        "token": token,
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    return response.json()
def get_last_messages():
    url = "http://localhost:5000/messages"
    r = requests.get(url)
    return r.json()
def get_message(id):
    if id == str:
        pass
    else:
        id = str(id)
    url = "http://localhost:5000/message/" + id
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
def delete_message(id):
    if id == str:
        pass
    else:
        id = str(id)
    url = "http://localhost:5000/message/" + id
    payload = json.dumps({
        "token": token
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers, data = payload)
    return response.json()
