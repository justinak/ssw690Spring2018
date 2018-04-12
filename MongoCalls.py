"""Handle calls to and from mongodb"""
from pymongo import MongoClient
import json
from random import randint
import datetime
from flask import jsonify

#client = MongoClient()
client = MongoClient('mongodb://duck_hacker:ssw690@34.230.77.217/ssw690spring2018')
db = client.ssw690spring2018

def add_user(id, email, uname, photo):
    try:
        db.Users.insert_one({
            'uuid':id,
            'email':email,
            'username':uname,
            'photo':photo
        })
    except Exception as e:
        print('ERROR ADDING USER', e)

def get_user():
    try:
        result = db.Users.find()
    except Exception as e:
       print('ERROR READING FILE', e)
    users = [post for post in result]
    return users


def get_specific_user(id):
    try:
        result = db.Users.find_one({'_id': id})
    except Exception as e:
       print('ERROR READING FILE', e)
    user = [post for post in result]
    return user


def get_question():
    """retrieve all the questions contained in Interview collection"""

    try:
        questions = db.Interview.find()
    except:
       print('ERROR READING FILE')
    brokendownexp = [post for post in questions]
    return brokendownexp


def insert_questions(question, title, topic):
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


def get_specific_ques(id):
    question = None
    try:
        question = db.Interview.find_one({'_id': int(id)})
    except Exception as e:
        print('Error finding element : {}'.format(e))

    result =[ques for ques in question]
    return result


def insert_experience(userid, exp):
    """insert user experience into Experience collection"""
    id = randint(0, 9999)
    try:
        db.Experience.insert_one(
        {
            '_id': id,
            'userid':userid,
            'experience': exp,
            'time': get_time(),
            "votes":0
        }
        )
    except Exception as e:
        print('Error submitting experience: {}'.format(e))


def get_experience():
    """retrieve all the experiences contained in Experience collection"""

    try:
        experience = db.Experience.find()
    except Exception as e:
       print('ERROR READING FILE:', e)

    result =[exp for exp in experience]
    return result


def get_solution():
    """retrieve all the solutions conatined in solutions collection"""
    try:
        solution = db.Solution.find()
    except:
        print('Error retrieving file')

    result = [sol for sol in solution]
    return result


def get_solution_by_id(id):
    solution = None
    table = db.Solution
    listofsol = []

    try:
        solution = table.find({'quesid': id})

    except Exception as e:
        print('Error finding element : {}'.format(e))
    for r in solution:
        listofsol.append(r)

    return listofsol


def insert_solution(solution, quesid, files=None):
    """insert solutions into the solution collection"""

    id = randint(0, 9999)
    try:
        db.Solution.insert_one(
        {
            '_id': id,
            "userid": 'hannah',
            'quesid':quesid,
            "files": files,
            "votes": 0,
            "solution": solution,
            'time': get_time()
        }
        )
    except Exception as e:
        print('Error submitting solution: {}'.format(e))


def find_by_topic(topic):
    table = db.Interview

    try:
        questions = table.find({'topic': topic})

    except Exception as e:
        print("Error finding element: {}".format(e))

    result = [ques for ques in questions]
    return result


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

