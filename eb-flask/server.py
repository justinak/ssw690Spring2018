# from flask import Flask


# # EB looks for an 'application' callable by default.
# app = Flask(__name__)




# @app.route("/videos")
# def video():
#     return 'Hello'


# # run the app.
# if __name__ == "__main__":
#     app.debug = True
#     app.run()

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'ssw690spring2018'
app.config['MONGO_URI'] = 'mongodb://34.228.66.29:27017/ssw690spring2018'
app.config['MONGO_USERNAME'] = 'duck_hacker'
app.config['MONGO_PASSWORD'] = 'ssw690'
app.config['MONGO_AUTH_MECHANISM'] = 'MONGODB-CR'

mongo = PyMongo(app)


@app.route('/')
def get_all_videos():
    '''Method returns all the videos on the database'''
    return jsonify({'result': 'videos'})

@app.route('/me', methods=['GET'])
def get_all_stars():
  star = mongo.db['MONGO_DBNAME']
  output = []
  d = star.find()
  print(d)
  if d:
    for s in star.find():
        output.append({'name' : s['name'], 'distance' : s['distance']})
    return jsonify({'result' : output})
  else:
    return jsonify({'result': 'Nothing Found'})

@app.route('/star/', methods=['GET'])
def get_one_star(name):
  data = mongo.db.ssw690spring2018
  s = data.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'distance' : s['distance']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

# @app.route('/star', methods=['POST'])
# def add_star():
#   star = mongo.db.stars
#   name = request.json['name']
#   distance = request.json['distance']
#   star_id = star.insert({'name': name, 'distance': distance})
#   new_star = star.find_one({'_id': star_id })
#   output = {'name' : new_star['name'], 'distance' : new_star['distance']}
#   return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)