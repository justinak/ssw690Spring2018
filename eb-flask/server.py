from flask import Flask, request, jsonify, abort, url_for, make_response, session
from flask_login import login_user, logout_user, LoginManager, login_required, current_user
from flask_pymongo import PyMongo
from random import randint
from auth.User import User
import settings
import re


app = Flask(__name__)

# App Sessions
app.config['SESSION_TYPE'] = settings.APP_SESSION_TYPE
app.config['SECRET_KEY'] = settings.APP_SECRET_KEY

# Mongo Configuration
app.config['MONGO_DBNAME'] = settings.MONGO_DBNAME
app.config['MONGO_HOST'] = settings.MONGO_HOST
app.config['MONGO_PORT'] = settings.MONGO_PORT
app.config['MONGO_USERNAME'] = settings.MONGO_USERNAME
app.config['MONGO_PASSWORD'] = settings.MONGO_PASSWORD
app.config['MONGO_AUTH_MECHANISM'] = settings.MONGO_AUTH_MECHANISM
mongo = PyMongo(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'please go to /videos to see all videos'

@app.route('/api/post/video', methods=['POST'])
def post_video():
    '''Method use to post video to S3 and store data in database'''

    return jsonify({'result': None})

@app.route('/videos', methods=['GET', 'POST'])
def get_all_videos():
    '''Method returns all the videos on the database'''
    output = []
    data = mongo.db.Videos.find()

    for d in data:
        output.append(d)

    return jsonify({'result': output})


@app.route('/videos/<name>', methods=['GET', 'POST'])
def get_one_video(name):
  data = mongo.db.Videos
  res = data.find_one({'name': name})

  if res:
    output = {'name': res['name']}
  else:
    output = "No such name"
  return jsonify({'result': output})


@app.route('/api/login', methods=['POST'])
def login():
    username = str(request.json.get('username')).lower()
    password = request.json.get('password')

    if username in session:
        return get_all_videos()

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
    user = User(user_to_validate['_id'], user_to_validate['full_name'], username, password)

    login_user(user)

    return get_all_videos()


@app.route('/api/new/users', methods = ['POST'])
def new_user():
    """Creates new user by providing json content of Full name, Username and Password"""
    full_name = request.json.get('full_name')
    username = str(request.json.get('username')).lower()
    password = request.json.get('password')
    id = randint(10000, 99999)

    if not re.match(settings.EMAIL_VALIDATION, username):
        return jsonify({'result': 'invalid email'})

    if username is None or password is None:
        return jsonify({'result': 'Field cannot be empty'})

    # Starting MongoDB
    userDB = mongo.db.Users

    if userDB.find_one({'username': username}) is not None:
        return jsonify({'result': 'username exist already, please select another.'})

    # Instantiate user
    user = User(id, full_name, username, password)
    # Inserting user to database
    userDB.insert({'_id': id,'full_name': user.full_name, 'username': user.username, 'password': user.get_password(), 'is_authenticated': user.is_authenticated(), 'is_active': user.is_active(), 'is_anonymous': user.is_anonymous()})

    return jsonify({'result': 'user created' }, 201, {'Location': url_for('new_user', id = user._id, _external = True)})


@login_manager.user_loader
def load_user(id):
    temp = mongo.db.Users.find_one({'_id': id})
    user = User(temp['_id'], temp['full_name'], temp['username'], temp['password'])
    return user.get_id()

@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        temp = mongo.db.Users.find_one({'_id': id})
        user = User(temp['_id'], temp['full_name'], temp['username'], temp['password'])
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('auth')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'result': 'log out Successfully {}'.format(login_user())})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)





if __name__ == '__main__':
    app.run(debug=True)
