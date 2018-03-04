from flask import Flask, request, flash, jsonify, abort
from flask_login import login_user, logout_user, LoginManager
from flask_pymongo import PyMongo
from auth.User import User
import settings
import re


app = Flask(__name__)

# Mongo Configuration
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['MONGO_DBNAME'] = settings.MONGO_DBNAME
app.config['MONGO_HOST'] = settings.MONGO_HOST
app.config['MONGO_PORT'] = settings.MONGO_PORT
app.config['MONGO_USERNAME'] = settings.MONGO_USERNAME
app.config['MONGO_PASSWORD'] = settings.MONGO_PASSWORD
app.config['MONGO_AUTH_MECHANISM'] = settings.MONGO_AUTH_MECHANISM

mongo = PyMongo(app)
login_manager = LoginManager()



@app.route('/', methods=['GET', 'POST'])
def index():
    return 'please go to /videos to see all videos'

@app.route('/videos', methods=['GET', 'POST'])
def get_all_videos():
    '''Method returns all the videos on the database'''
    output = []
    data = mongo.db.Users.find()

    for d in data:
        output.append(d)

    return jsonify({'result': output})


@app.route('/videos/<name>', methods=['GET', 'POST'])
def get_one_video(name):
  data = mongo.db.videos
  s = data.find_one({'name' : name})

  if s:
    output = {'name' : s['name']}
  else:
    output = "No such name"
  return jsonify({'result': output})


@app.route('/api/login', methods=['POST'])
def login():
    username = str(request.json.get('username')).lower()
    password = request.json.get('password')

    if not re.match(settings.EMAIL_VALIDATION, username):
        return jsonify({'result': 'invalid email'})

    if username is None or password is None:
        return jsonify({'result': 'invalid username and/or password'})

    # Starting MongoDB
    userDB = mongo.db.Users

    if not userDB.find_one({'username': username}):
        return jsonify({'result': 'invalid username'})

    user_to_validate = userDB.find_one({'username': username})

    if not User.verify_password(password, user_to_validate['password']):
        return jsonify({'result': 'invalid password'})

    # Instantiate user
    user = User(user_to_validate['full_name'], username, password)

    login_user(user)

    Flask.flash('Logged in successfully.')
    next = Flask.request.args.get('next')

    if not is_safe_url(next):
        return abort(400)

    return get_all_videos()


@app.route('/api/new/users', methods = ['POST'])
def new_user():
    """Creates new user by providing json content of Full name, Username and Password"""
    full_name = request.json.get('full_name')
    username = str(request.json.get('username')).lower()
    password = request.json.get('password')

    if not re.match(settings.EMAIL_VALIDATION, username):
        return jsonify({'result': 'invalid email'})

    if username is None or password is None:
        return jsonify({'result': 'Field cannot be empty'})

    # Starting MongoDB
    userDB = mongo.db.Users

    if userDB.find_one({'username': username}) is not None:
        return jsonify({'result': 'username exist already, please select another.'})

    # Instantiate user
    user = User(full_name, username, password)

    # Inserting user to database
    userDB.insert({'full_name': user.full_name,'username': user.get_id(), 'password': user.get_password()})

    return jsonify({'result': 'user created' })

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'result': 'log out Successfully'})


if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(debug=True)
