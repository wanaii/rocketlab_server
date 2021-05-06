from flask import Flask
from pymongo import MongoClient
from flask import request
import json


CLIENT = MongoClient('mongodb://127.0.0.1:27017')

FLASK_DB = CLIENT.rocketlab
USER_DB = FLASK_DB.users
CONTENT_DB = FLASK_DB.contents

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testinsert', methods=['POST'])
def testInsert():
    USER_DB.insert_one({'username': 'test', 'password': '111111'})
    return 'success'

@app.route('/signup', methods=['POST'])
def signup():
    try:
        body = json.loads(request.data.decode('utf-8'))
        username = body['username']
        password = body['password']

    except e:
        print(e)
    if USER_DB.find({'username': username}).count() == 0:
        USER_DB.insert_one({'username': username, 'password': password})
        return {
            'code': 200,
            'data': 'success',
        }
    else:
        return {
            'code': 400,
            'data': 'failed',
        }

@app.route('/login', methods=['POST'])
def login():
    try:
        body = json.loads(request.data.decode('utf-8'))
        username = body['username']
        password = body['password']
    except e:
        print(e)
    if USER_DB.find({'username': username, 'password': password}).count() == 0:
        return {
            'code': 400,
            'data': 'failed',
        }
    else:
        return {
            'code': 200,
            'data': 'success',
        }

@app.route('/save', methods=['POST'])
def save():
    try:
        body = json.loads(request.data.decode('utf-8'))
        username = body['username']
        userdata = body['userdata']
    except e:
        print(e)
    if CONTENT_DB.find({'username': username}).count() > 0:
        CONTENT_DB.delete_one({'username': username})
    CONTENT_DB.insert_one({'username': username, 'userdata': userdata})
    return {
        'code': 200,
        'data': 'success',
    }

@app.route('/restore', methods=['POST'])
def restore():
    try:
        body = json.loads(request.data.decode('utf-8'))
        username = body['username']
    except e:
        print(e)
    print(type(json.loads(CONTENT_DB.find_one({'username': username})['userdata'])))
    return {
        'code': 200,
        'data': json.loads(CONTENT_DB.find_one({'username': username})['userdata']),
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
