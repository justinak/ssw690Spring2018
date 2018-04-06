from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
import eb_flask.settings as settings

app = Flask(__name__)

# App Sessions
app.config['SESSION_TYPE'] = settings.APP_SESSION_TYPE
app.config['SECRET_KEY'] = settings.APP_SECRET_KEY

# Mongo Configuration for production
app.config['MONGO_DBNAME'] = settings.MONGO_DBNAME
app.config['MONGO_HOST'] = settings.MONGO_HOST
app.config['MONGO_PORT'] = settings.MONGO_PORT
app.config['MONGO_USERNAME'] = settings.MONGO_USERNAME
app.config['MONGO_PASSWORD'] = settings.MONGO_PASSWORD
app.config['MONGO_AUTH_MECHANISM'] = settings.MONGO_AUTH_MECHANISM

mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'please go to /videos to see all videos'


@app.route('/api/post/video', methods=['POST'])
def post_video():
    """Method use to post video to S3 and store data in database"""

    print(request.json)

    return jsonify({'result': None})


@app.route('/videos', methods=['GET'])
def get_all_videos():
    """Method returns videos that match the search title in the database"""
    output = []
    name = request.args.get('name')
    print(name)
    data = mongo.db.Videos.find({'title': name}) # Use find, not find_one
    print(data)
    if data:
        for d in data:
            d['_id'] = str(d['_id'])
            output.append(d)
        return jsonify({'result': output})
    else:
        return jsonify({'result': output})


@app.route('/feeds', methods=['GET'])
def get_all_feeds():
    """Method returns all the feeds on the database"""
    output = []
    data = mongo.db.Feeds.find()

    for d in data:
        output.append(d)

    return jsonify({'result': output})


@app.route('/new/feed', methods=['POST'])
def post_feed():
    feed = mongo.db.Feeds
    actor = request.json['actor']
    verb = request.json['verb']
    object = request.json['object']
    target = request.json['target']
    foreign_id = request.json['foreign id']
    time = request.json['time']
    message = request.json['message']
    feed_id = feed.insert(
        {'actor': actor, 'verb': verb, 'object': object, 'target': target, 'foreign id': foreign_id, 'time': time,
         'message': message})
    new_feed = feed.find_one({'_id': feed_id})
    output = {'actor': new_feed['actor'], 'verb': new_feed['verb'], 'object': new_feed['object'],
              'target': new_feed['target'], 'foreign id': foreign_id, 'time': time, 'message': message}
    return jsonify({'result': output})


@app.route('/api/new/users', methods=['POST'])
def new_user():
    """Creates new user by providing json content of Full name, Username and Password"""
    uid = request.json.get('uuid')
    email = request.json.get('email')
    # Starting MongoDB
    user_db = mongo.db.Users
    print(uid, email)
    # Inserting user to database
    user_db.insert({'uuid': uid, 'email': email})

    return jsonify({'result': 'user created'})


@app.route('/api/NewPost', methods=['POST'])
def new_feed_post():
    """Creates NewPost by providing json content of ID and postBody"""
    user_id = request.json.get('uuid')
    post_body = request.json.get('text')
    posts_db = mongo.db.Posts
    posts_db.insert({'uuid': user_id, 'text': post_body})
    return jsonify({'result': 'Post Created'})


@app.route('/api/posts/get', methods=['GET'])
def get_post():
    """Grabs all posts"""

    output = []
    user_id = request.args.get('uuid')
    data = mongo.db.Posts.find({'uuid': user_id })

    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})


@app.route('/api/get/timeline', methods=['GET'])
def get_timeline():
    """
    Get someone's timeline
    Request uuid(user)
    """
    output = []
    data1 = []
    data2 = []
    post = mongo.db.Posts
    user = mongo.db.Users
    uuid = request.args.get('uuid')
    data = user.find({'uuid': uuid})

    for i in data:

        data1.append(i)

    for n in data1:
        x = post.find({'uuid': n})

        for m in x:
            data2.append(m)

    for d in data2:
        d['_id'] = str(d['_id'])
        output.append(d)

    print(output)

    return jsonify({'result': output})


@app.route('/api/users/get', methods=['GET'])
def get_users():
    """Grabs all users"""

    output = []
    data = mongo.db.Users.find()

    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
