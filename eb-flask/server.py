from flask import Flask, request, jsonify, make_response, render_template
from flask_pymongo import PyMongo
from googleapiclient.discovery import build
import boto3
from botocore.client import Config
import argparse
import datetime
import settings

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

# extensions
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'please go to /videos for all videos'

#
# # Video Routes
# @app.route('/videos/templates')
# def test_videos_with_template():
#     output = []
#     data = mongo.db.Videos.find({})
#     youtube_data = youtube_api()
#
#     for d in data:
#         d['_id'] = str(d['_id'])
#         output.append(d)
#
#     output.extend(youtube_data)
#
#     return render_template('hola.html', videos=output)


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



@app.route('/api/videos', methods=['GET'])
def get_all_videos():
    """Method returns all the videos on the database as well as youtube"""
    output = []

    data = mongo.db.Videos.find({})

    for source_a in data:
        source_a['_id'] = str(source_a['_id'])
        output.append(source_a)

    # Get youtube videos and add to output list
    youtube_data = youtube_api()
    output.extend(youtube_data)

    return jsonify({'result': output})


@app.route('/api/videos/<title>', methods=['GET', 'POST'])
def get_videos_containing_title(title):
    """Method returns all videos containing the title from the database"""
    data = mongo.db.Videos
    output = []

    for d in data.find({'title': { '$regex' : title, '$options' : 'i' }}):
        d['_id'] = str(d['_id'])
        output.append(d)

    if not output:
        return jsonify({'result': 'Not Found'})

    return jsonify({'result': output})

@app.route('/api/uservideos', methods=['POST'])
def get_videos_containing_user_id():
    """Method returns all videos for a particular user base on the people they follow an array of users must be pass"""

    if request.method == "POST":
        data = mongo.db.Videos

        user_id = str(request.json.get('user_id')).upper()
        output = []

        for d in data.find({'user_id': user_id }):
            d['_id'] = str(d['_id'])
            output.append(d)

        if not output:
            return jsonify({'result': 'Not Found'})

        return jsonify({'result': output})

# Videos Services
def youtube_api(query="Stevens Institute of Technology"):
    """Helper function to the youtube_search"""
    data = youtube_search(query)
    return data


def youtube_search(query):
    """Performs youtube search for the search key that's passed"""
    youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
        developerKey=settings.DEVELOPER_KEY)

    # Arguments to be use to pass to youtube
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=query)
    parser.add_argument('--max-results', help='Max results', default=50)
    args = parser.parse_args()

    # youtube call
    search_response = youtube.search().list(
        q=args.q,
        part='id,snippet',
        type='video',
        maxResults=args.max_results
    ).execute()

    videos = []

    # collect the data from youtube place it in a dictionary and append it to the video list
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_data = dict()
            id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            description = search_result['snippet']['description']
            src = 'https://www.youtube.com/embed/'+id
            publish_date = search_result['snippet']['publishedAt']
            video_data['_id'] = str(id)
            video_data['title'] = title
            video_data['description'] = description
            video_data['src'] = src
            video_data['publish_date'] = publish_date
            videos.append(video_data)
            del video_data

    return videos

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



# picture for post


def post_picture_for_post_to_mongo(file, request):
    """Uploads Picture data to database"""
    try:
        Posts = mongo.db.Posts
        Posts.insert(
            {
                'uuid': str(request.form.get('user_id')).upper(),
                'created_by': str(request.form.get('created_by')).upper(),
                'text': request.form.get('text'),
                'image': 'http://d1nmi5ea5e2ysf.cloudfront.net/'+file.filename,
                'description': request.form.get('description'),
                'time': datetime.datetime.now()
              })

    except Exception as e:
        return e


def upload_picture_for_post_to_S3(file, file_name):
    """Uploads Pictures to s3 """
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
    """Page not found"""
    return make_response(jsonify({'error': 'Page Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host="155.246.44.87")
