"""Handle calls to and from mongodb"""
from pymongo import MongoClient
import json
from random import randint
import datetime
from flask import jsonify

#client = MongoClient()
client = MongoClient('mongodb://duck_hacker:ssw690@34.230.77.217/ssw690spring2018')
db = client.ssw690spring2018


def get_question():
    """retrieve all the questions contained in Interview collection"""

    try:
        questions = db.Interview.find()
    except:
       print('ERROR READING FILE')
    brokendownexp = [post for post in questions]
    return brokendownexp


def get_experience():
    """retrieve all the experiences contained in Experience collection"""

    try:
        experience = db.Experience.find()
    except :
       print('ERROR READING FILE')
    return experience


def get_solution():
    """retrieve all the solutions conatined in solutions collection"""
    try:
        solution = db.Solution.find()
    except:
        print('Error retrieving file')

    return solution


def insert_solution(solution, id, files=None):
    """insert solutions into the solution collection"""

    id = randint(0, 9999)
    try:
        db.Solution.insert_one(
        {
            '_id': id,
            "userid": 'hannah',
            "files": files,
            "votes": 0,
            "solution": solution,
            'time': get_time()
        }
        )
    except Exception as e:
        print('Error submitting solution: {}'.format(e))


def insert_interview(question, title, topic):
    """insert solutions into the solution collection"""

    id = randint(0, 9999)
    try:
        db.Interview.insert_one(
        {
            '_id': id,
            'title': title,
            "votes": 0,
            "question": question,
            'topic': topic,
            'userid': 'hannah',
            'time': get_time()
        }
        )
    except Exception as e:
        print('Error submitting solution: {}'.format(e))


def insert_experience(experience, files=''):
    """insert user experience into Experience collection"""

    id=randint(0, 9999)
    try:
        db.Experience.insert_one(
        {
            '_id': id,
            "userid": 'hannah',
            "files": files,
            "votes": 0,
            "Experience": experience,
            'time': get_time()
        }
        )
    except Exception as e:
        print('Error submitting experience: {}'.format(e))


def find_by_topic(topic):
    table = db.Interview

    try:
        questions = table.find({'topic': topic})

    except Exception as e:
        print("Error finding element: {}".format(e))

    return questions


def increase_count(post_id):
    """increase count of votes by 1"""

    votes=None
    table = db.Solution

    try:
        solution = table.find_one({'_id': int(post_id)})
        votes = solution['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes)+1

    try:
        db.Solution.update_one(
        {'_id': int(post_id)},
        {"$set":{"votes" : new_vote}
          }
        )
    except Exception as e:
        print('Error updating count: {}'.format(e))


def decrease_count(post_id):
    """decrease count of votes by 1"""
    votes = None
    table = db.Solution

    try:
        solution = table.find_one({'_id': int(post_id)})
        votes = solution['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes) - 1
    try:
        db.Solution.update_one(
            {'_id': int(post_id)},
            {"$set": {"votes" : new_vote}
             }
        )
    except Exception as e:
        print('Error updating count: {}'.format(e))


def ex_increase_count(post_id):
    """increase count of votes by 1"""

    votes=None
    table = db.Experience

    try:
        Experience = table.find_one({'_id': int(post_id)})
        votes = Experience['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes)+1

    try:
        db.Experience.update_one(
        {'_id': int(post_id)},
        {"$set":{"votes" : new_vote}
          }
        )
    except Exception as e:
        print('Error updating count: {}'.format(e))


def ex_decrease_count(post_id):
    """decrease count of votes by 1"""
    votes = None
    table = db.Experience

    try:
        Experience = table.find_one({'_id': int(post_id)})
        votes = Experience['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes) - 1
    try:
        db.Experience.update_one(
            {'_id': int(post_id)},
            {"$set": {"votes" : new_vote}
             }
        )
    except Exception as e:
        print('Error updating count: {}'.format(e))


def download_file(filename):
    """download file uploaded to mongodb"""
    try:
        post = db.solution.find({"file":filename})
    except Exception as e:
        print('Error downloading file: {}'.format(e))
    return post.file

def get_ex_votes(post_id):
    votes = None
    table = db.Experience
    try:
        Experience = table.find_one({'_id': int(post_id)})
        votes = Experience['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    return votes

def get_time():
    return datetime.datetime.now()

