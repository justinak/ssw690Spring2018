from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for
from flask_pymongo import PyMongo
import eb_flask.settings as settings
import datetime
from random import randint
import boto3
from botocore.client import Config
from bson.binary import Binary
#from Firebase_config import user_unique
import MongoCalls
import os


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
    return render_template('Login.html', title=title)


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


@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method =="POST":
        email = request.form['user_unique_email']
        password = request.form['user_unique_pswrd']
        global user_unique
        user_unique = user_unique(email, password)
        token = user_unique.signin()
        if token != None:
            return redirect(url_for('get_questions'))

    return redirect(url_for('Index'))


@app.route('/signup',methods=['POST', 'GET'])
def sign():
    if request.method =="POST":
        email = request.form['user_unique_email']
        password = request.form['user_unique_pswrd']
        user_uniquename = request.form['user_unique_name']
        global user_unique
        user_unique = user_unique(email, password)
        token = user_unique.create_user_unique()

        if token != None:
            MongoCalls.add_user_unique(token, email, user_uniquename,
                                       'https://pbs.twimg.com/profile_images/676830491383730177/pY-4PfOy_400x400.jpg')
            return redirect(url_for('get_questions'))

    return redirect(url_for('Index'))


@app.route('/menu', methods=['POST', 'GET'])
def menu_options():
    """Handle clicks of menu options ***still needs to be updated"""
    if request.method == 'POST':
        if request.form['menu'] == 'Experience':
            return redirect(url_for('display_experiences'))
        if request.form['menu'] == 'newQuestion':
            return redirect(url_for('display_add_question'))
        if request.form['menu'] == 'Questions':
            return redirect(url_for('get_questions'))
        if request.form['menu'] == 'Topics':
            return redirect(url_for('display_topic'))

################################################################################################
@app.route('/questions')
def get_questions():
    global post_questions
    questions = MongoCalls.get_question()
    randnum = randint(0, len(questions) - 1)
    post_questions['question'] = questions[randnum]
    solutions = MongoCalls.get_solution_by_id(questions[randnum]['_id'])
    return render_template('DuckHacker.html', title=title, question=questions[randnum],
                           newcomment=solutions)


#######################################################################################################
@app.route('/comment', methods=['POST', 'GET'])
def handle_data():

    if request.method == 'POST':
        answer = request.form['Solution']
        id = request.form['quesid']
        if 'file' not in request.files:
            MongoCalls.insert_solution(answer, id)
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_solution(answer, id, files=binfile)
        solutions = MongoCalls.get_solution_by_id(id)
        question = MongoCalls.get_specific_ques(id)
    elif request.method =='GET':
        id=request.form['quesid']
        solutions = MongoCalls.get_solution_by_id(id)
        question = MongoCalls.get_specific_ques(id)

        # return render_template('DuckHacker.html', title=title, question=post_questions['question'],
        #                        newcomment=MongoCalls.get_solution_by_id(8345))
    return render_template('DuckHacker.html', title=title, question=question, newcomment=solutions)


#########################################################################################################
@app.route('/question/add')
def display_add_question():
    return render_template('Questions.html')

########################################################################################################
@app.route('/experience')
def display_experiences():
    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


############################################################################################################
@app.route('/experience/submit', methods=['POST', 'GET'])
def experience():
    id = randint(0, 9999)
    if request.method == 'POST':
        projectpath = request.form['Experience']
        if 'file' not in request.files:

            MongoCalls.insert_experience(id, projectpath)
            # Experiences_page.add_experience(projectpath, id)
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_experience(id, projectpath)
                # Experiences_page.add_experience(projectpath, id)

    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


########################################################################################################
@app.route('/question/submit', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        projectpath = request.form['question']
        title = request.form['title']
        topic = request.form['topic']
        MongoCalls.insert_questions(projectpath, title, topic)

    return redirect(url_for('get_questions'))


#############################################################################################################
@app.route('/question/topic', methods=['POST', 'GET'])
def get_topic_questions():
    questions = None
    if request.method == 'POST':

        if request.form['topic'] == 'Algorithm':
            questions =MongoCalls.find_by_topic('Algorithm')
        elif request.form['topic'] == 'DataAnalysis':
            questions = MongoCalls.find_by_topic('DataAnalysis')
        elif request.form['topic'] == 'SoftwareEngineering':
            questions = MongoCalls.find_by_topic('Software Engineering')
        elif request.form['topic'] == 'SystemsEngineering':
            questions = MongoCalls.find_by_topic('System Engineering')
        elif request.form['topic'] == 'Testing':
            questions = MongoCalls.find_by_topic('Testing')

    return render_template('Topics.html', title=title, questions=questions)


#########################################################################################################
@app.route('/topic/question', methods =['POST', 'GET'])
def display_question_id():
    if request.method == 'POST':
        ques_id = request.form['solve']
        question = MongoCalls.get_specific_ques(ques_id)
        global post_questions
        post_questions['question'] = question
        solutions = MongoCalls.get_solution_by_id(ques_id)
        return render_template('DuckHacker.html', title = title, question=question, newcomment=solutions)
    return('Not found')


##########################################################################################################
@app.route('/topic')
def display_topic():
    return render_template('Topics.html', title=title)


#############################################################################################################
@app.route('/voteup/<string:post_id>', methods=['POST'])
def voteUp(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.increase_count(post_id)
    solutions = MongoCalls.get_solution_by_id(post_questions['question']['_id'])
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


##########################################################################################################
@app.route('/votedown/<string:post_id>', methods=['POST'])
def votedown(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.decrease_count(post_id)
    solutions = MongoCalls.get_solution_by_id(post_questions['question']['_id'])
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


#########################################################################################################
@app.route('/exvoteup/<string:post_id>', methods=['POST'])
def ex_voteUp(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.ex_increase_count(post_id)
    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


##########################################################################################################
@app.route('/exvotedown/<string:post_id>', methods=['POST'])
def ex_votedown(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.ex_decrease_count(post_id)
    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


########################################################################################################
@app.route('/downloads/')
def download_file(filename):
    """Method to handle downloads of files"""
    file = MongoCalls.download_file(filename=filename)
    read_file = make_response(file.read())
    read_file.headers['Content-Type'] = 'application/octet-stream'
    read_file.headers["Content-Disposition"] = "attachment; filename={}".format(filename)

    return read_file

def save_file(file):
    target = os.path.join(App_root, 'uploads/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if file.filename:
        destination = "/".join([target, file.filename])
        file.save(destination)
        return convert_binary(destination)


def convert_binary(file):
    """function to convert file passed to binary file"""
    with open(file, 'rb') as fil:
        f = fil.read()
        encoded_file = Binary(f, 0)

    return encoded_file


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
