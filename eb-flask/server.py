from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import settings

app = Flask(__name__)

# Mongo Configuration
app.config['MONGO_DBNAME'] = settings.MONGO_DBNAME
app.config['MONGO_HOST'] = settings.MONGO_HOST
app.config['MONGO_PORT'] = settings.MONGO_PORT
app.config['MONGO_USERNAME'] = settings.MONGO_USERNAME
app.config['MONGO_PASSWORD'] = settings.MONGO_PASSWORD
app.config['MONGO_AUTH_MECHANISM'] = settings.MONGO_AUTH_MECHANISM

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'please go to /videos to see all videos'

@app.route('/videos', methods=['GET'])
def get_all_videos():
    '''Method returns all the videos on the database'''
    output = []
    data = mongo.db.videos.find()

    for d in data:
        output.append(d)

    return jsonify({'result': output})


@app.route('/videos/<name>', methods=['GET'])
def get_one_video(name):
  data = mongo.db.videos
  s = data.find_one({'name' : name})

  if s:
    output = {'name' : s['name']}
  else:
    output = "No such name"
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)
