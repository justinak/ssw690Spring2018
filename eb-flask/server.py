from flask import Flask, request, jsonify, make_response, render_template, json
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth
from googleapiclient.discovery import build
import boto3
import pprint
from botocore.client import Config
from random import randint
import argparse
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
auth = HTTPBasicAuth()


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'please go to /videos/youtube to see stevens videos from youtube or /videos for all videos'

# Video Routes

@app.route('/videos/youtube')
def youtubeApi():
    data = youtube_search()
    return data


def youtube_search():
    youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
        developerKey=settings.DEVELOPER_KEY)

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Stevens Institute of Tech')
    parser.add_argument('--type', help='video', default='video')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()


    search_response = youtube.search().list(
        q=args.q,
        part='id,snippet',
        maxResults=args.max_results
    ).execute()

    v = dict()
    t = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            id = search_result['snippet']
            title = search_result['snippet']['title']
            src = search_result['snippet']['thumbnails']['high']
            publish_date = search_result['snippet']['publishedAt']
            v['_id'] = id
            v['title'] = title
            v['src'] = src
            v['publish_date'] = publish_date
            t.append(v)

    return t

@app.route('/api/post/video', methods=['POST', 'GET'])
def post_video():
    '''Method use to post video to S3 and store data in database'''

    if request.method == 'POST':
        file = request.files['file']

        video_format_list = ('.mp4')

        if file is not None and file.filename.endswith(video_format_list):
            post_video_to_mongo(file)
            upload_video_to_S3(file, file.filename)
        else:
            result = {
                'message': 'check file and try again, ',
                'uploaded': 'false'
            }

        data = youtubeApi()

        return render_template('hola.html', videos=data)

    return render_template('video.html')

def post_video_to_mongo(file):
    '''Uploads video data to database'''
    try:
        id = randint(10000, 99999)
        videoDB = mongo.db.Videos
        video_name = file.filename.split('.')
        videoDB.insert(
            { '_id': id,
              'title': video_name[0],
              'src': settings.AWS_BASE_URL+video_name
              })

    except Exception as e:
        return e

def upload_video_to_S3(file, file_name):
    '''Uploads video to s3 '''
    try:
        # S3 Connect
        s3 = boto3.resource( 's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
        )

        s3.Bucket(settings.BUCKET_NAME).put_object(Key=file_name, Body=file)
    except Exception as e:
        print("Something wrong happened", e)
        return e


@app.route('/videos', methods=['GET', 'POST'])
def get_all_videos():
    '''Method returns all the videos on the database'''
    output = []
    data = mongo.db.Videos.find()

    pprint.pprint(data)

    for d in data:
        output.append(d)

    other_videos = youtubeApi()

    for v in other_videos:
        output.append(v)

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



if __name__ == '__main__':
    app.run(debug=True)
