from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
import eb_flask.settings as settings
import datetime
from random import randint
import boto3
from botocore.client import Config

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


# @app.route('/api/post/video', methods=['POST', 'GET'])
# def post_video():
#     """Method use to post video to S3 and store data in database"""
#
#     file = request.files['file']
#     return jsonify(file)



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


@app.route('/api/new/user', methods=['POST'])
def new_user():
    """Creates new user by providing json content
    of Full name, Username and Password"""
    uuid = request.json.get('uuid')
    email = request.json.get('email')
    at_symbol = email.find('@')
    username = email[:at_symbol]
    photo = "https://pbs.twimg.com/profile_images/676830491383730177/pY-4PfOy_400x400.jpg"
    user = mongo.db.Users
    print(uuid, email)
    follow = []
    follower = []
    likes = []
    if user.find_one({'uuid': uuid}) is not None:
        return jsonify({'result': 'uuid is already exist'})

    user.insert({'uuid': uuid, 'email': email, 'username': username, 'photo': photo, 'follow': follow, 'follower': follower, 'likes': likes})

    return jsonify({'result': "User created"})



@app.route('/api/new/post', methods=['POST'])
def new_feed_post():
    """Creates NewPost by providing json content of ID and postBody"""
    uuid = request.json.get('uuid')
    text = request.json.get('text')
    user = mongo.db.Users
    post = mongo.db.Posts
    # image = request.json['image']
    user_document = user.find_one({'uuid': uuid})
    created_by = user_document['username']
    time = datetime.datetime.utcnow()
    likes = []
    post.insert({'uuid': uuid, 'created_by': created_by, 'text': text, 'image': "", 'time': time, 'likes': likes})
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


@app.route('/api/posts/get-username', methods=['GET'])
def get_post_username():
    """Grabs all posts based on created_by field i.e, the username"""

    output = []
    user_name = request.args.get('created_by')
    data = mongo.db.Posts.find({'created_by': user_name })

    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})


#  Kevin's routes
@app.route('/api/get/posts', methods=['GET'])
def get_posts():
    """
    Get all posts in MongoDB
    """
    post = mongo.db.Posts
    data = post.find()

    output = []
    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})


@app.route('/api/follow', methods=['PUT'])
def follow():
    """
    Follow people
    Request uuid(user), foreign_uuid(another user)
    """
    user = mongo.db.Users
    uuid = request.json['uuid']
    foreign_uuid = request.json['foreign_uuid']
    user.update({'uuid': uuid}, {"$addToSet": {'follow': foreign_uuid}}, True)
    user.update({'uuid': foreign_uuid}, {"$addToSet": {'follower': uuid}}, True)

    return jsonify({'result': "Follow successful!"})


@app.route('/api/unfollow', methods=['PUT'])
def unfollow():
    """
    Unfollow people
    Request uuid(user), foreign_uuid(another user)
    """
    user = mongo.db.Users
    uuid = request.json['uuid']
    foreign_uuid = request.json['foreign_uuid']
    user.update({'uuid': uuid}, {"$pull": {'follow': foreign_uuid}}, True)
    user.update({'uuid': foreign_uuid}, {"$pull": {'follower': uuid}}, True)

    return jsonify({'result': "Unfollow successful!"})


@app.route('/api/get/follow', methods=['GET'])
def get_follow_uuid():
    """
    Get uuid which someone followed
    Request uuid(user)
    """
    user = mongo.db.Users
    uuid = request.args.get('uuid')
    data = user.find_one({'uuid': uuid})
    if data:
        output = {'follow': data['follow']}
    else:
        output = ['Wrong uuid']
    return jsonify({'result': output})


@app.route('/api/get/follower', methods=['GET', 'POST'])
def get_follower_uuid():
    """
    Get someone's followers' uuid
    Request uuid(user)
    """
    user = mongo.db.Users
    uuid =request.json['uuid']
    data = user.find_one({'uuid': uuid})
    if data:
        output = {'follower': data['follower']}
    else:
        output = ['Wrong uuid']
    return jsonify({'result': output})


@app.route('/api/like', methods=['POST', 'GET'])
def like():
    """
    Like a post
    Request uuid(user), _id(post)
    """
    post = mongo.db.Posts
    user = mongo.db.Users
    _id = request.json['_id']
    uuid = request.json['uuid']
    post.update({'_id': ObjectId(_id)}, {"$addToSet": {'likes': uuid}}, True)
    user.update({'uuid': uuid}, {"$addToSet": {'likes': _id}}, True)

    return jsonify({'result': 'like it!'})


@app.route('/api/unlike', methods=['POST', 'GET'])
def unlike():
    """
    Unlike a post
    Request uuid(user), _id(post)
    """
    post = mongo.db.Posts
    user = mongo.db.Users
    _id = request.json['_id']
    uuid = request.json['uuid']
    post.update({'_id': ObjectId(_id)}, {"$pull": {'likes': uuid}}, True)
    user.update({'uuid': uuid}, {"$pull": {'likes': _id}}, True)

    return jsonify({'result': 'like it!'})


@app.route('/api/delete/post', methods=['DELETE'])
def delete_post():
    """
    Delete a post
    Request _id(post)
    """
    post = mongo.db.Posts
    _id = request.json['_id']
    post.delete_one({'_id': ObjectId(_id)})

    return jsonify({'result': "Post deleted!"})


@app.route('/api/get/timeline',methods=['GET', 'POST'])
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
        data1 = i['follow']

    for n in data1:
        x = post.find({'uuid': n})

        for m in x:
            data2.append(m)

    for d in data2:
        d['_id'] = str(d['_id'])
        output.append(d)

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



@app.route('/api/user/getone', methods=['GET'])
def get_one_user():
    """Grabs one user"""

    output = []
    uuid = request.args.get('uuid')
    data = mongo.db.Users.find({'uuid': uuid})

    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})


@app.route('/api/users', methods=['GET'])
def get_videos_containing_title():
    """Method returns all users containing the title from the database"""
    data = mongo.db.Users
    output = []
    username = request.args.get('username')
    for d in data.find({'username': { '$regex' : username, '$options' : 'i' }}):
        d['_id'] = str(d['_id'])
        output.append(d)

    if not output:
        return jsonify({'result': 'Not Found'})

    return jsonify({'result': output})

#Retrieve Experiences Route for iOS
@app.route('/api/get/experiences', methods=['GET'])
def get_experiences():
    """
    Get all experiences in MongoDB
    """
    post = mongo.db.Experience
    data = post.find()

    output = []
    for d in data:
        d['_id'] = str(d['_id'])
        output.append(d)

    return jsonify({'result': output})

@app.route('/api/new/experiences', methods=['POST'])
def new_experience_post():
    """Creates NewPost experience by providing json content of ID and postBody"""
    text = request.json.get('experience')
    userid = request.json.get('userid')
    votes = 0
    randomid = randint(0, 9999)
    exp = mongo.db.Experience
    time = datetime.datetime.utcnow()
    exp.insert({'_id': randomid ,'experience': text, 'time': time, 'votes': votes, 'userid': userid})
    return jsonify({'result': 'Experience Post Created'})


@app.route('/api/post/video', methods=['POST'])
def post_video():
    """Method use to post video to S3 and store data in database"""
    output = list() # List of videos to be return once uploaded
    if request.method == 'POST':

        file = request.files['file']

        video_format_list = ('.MP4', '.MOV')

        if file is not None and file.filename.upper().endswith(video_format_list):
            post_video_to_mongo(file, request)
            upload_video_to_S3(file, file.filename)

            result = {
                'message': 'uploaded',
                'uploaded': 'True'
            }
        else:
            result = {
                'message': 'check file and try again',
                'uploaded': 'false'
            }

        output.append(result)

    return jsonify({'result': output})



def post_video_to_mongo(file, request):
    """Uploads video data to database"""
    try:
        videoDB = mongo.db.Videos
        videoDB.insert(
            {
                'user_id': str(request.form.get('user_id')).upper(),
                'title': request.form.get('title'),
                'src': 'http://d1nmi5ea5e2ysf.cloudfront.net/'+file.filename,
                'description': request.form.get('description'),
                'publish_date': datetime.datetime.now()
            })

    except Exception as e:
        return e

def upload_video_to_S3(file, file_name):
    """Uploads video to s3 """
    try:
        # S3 Connect
        s3 = boto3.resource( 's3',
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             config=Config(signature_version='s3v4'),
                             )

        # adding file to S3
        s3.Bucket(settings.BUCKET_NAME).put_object(Key=file_name, Body=file)
    except Exception as e:
        print("Something wrong happened", e)
        return e


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)