# from flask import Flask, jsonify, render_template
# from flask_pymongo import PyMongo
#
#
# app = Flask(__name__)
#
#
# # Mongo Configuration
# app.config['MONGO_DBNAME'] = 'ssw690spring2018'
# app.config['MONGO_HOST'] = '34.228.66.29'
# app.config['MONGO_PORT'] = '27017'
# app.config['MONGO_USERNAME'] = 'duck_hacker'
# app.config['MONGO_PASSWORD'] = 'ssw690'
# app.config['MONGO_AUTH_MECHANISM'] = 'MONGODB-CR'
# mongo = PyMongo(app)
#
#
# @app.route('/justina', methods=['GET', 'POST'])
# def index():
#     output = []
#     data = mongo.db.Users.find()
#
#     for d in data:
#         output.append(d)
#
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

import boto3
from botocore.client import Config
import settings

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'ssw690spring2018'
FILE_NAME = 'youtubeapi.py';


data = open(FILE_NAME, 'rb')

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)

# Image download
s3.Bucket(BUCKET_NAME).put_object(Key='youtubeapi.py', Body=data)
# s3.Bucket(BUCKET_NAME).download_file(FILE_NAME, './downloads/bitmoji.png'); # Change the second part
# This is where you want to download it too.

print ("Done")
