from flask import Flask, request, jsonify, abort, url_for, make_response, session
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from flask_pymongo import MongoClient
from random import randint
from eb_flask.auth import User
import re
import eb_flask.settings as settings

# connect to database
connection = MongoClient('localhost', 27017)
db = connection.test
collection1 = db.posts
collection2 = db.users


app = Flask(__name__)


@app.route('/api/get/allposts', methods=['GET'])
def get_post():
    output = []
    data = collection1.find()

    for d in data:
        d['_id'] = str(['_id'])
        output.append(d)

    return jsonify({'result': output})


@app.route('/api/get/followposts', methods=['POST', 'GET'])
def get_user():
    uuid = request.json['uuid']
    output = []
    data2 = []
    data1 = []
    x = []

    data = collection2.find({"uuid": uuid})
    for i in data:
        data1 = i["follow"]
    for n in data1:
        x = collection1.find({"uuid": n})
    for m in x:       
        data2.append(m)       

    for d in data2:
        d['_id'] = str(['_id'])
        output.append(d)

    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
