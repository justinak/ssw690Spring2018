"""Handle calls to and from mongodb"""
from pymongo import MongoClient
import json
from random import randint
# client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
client = MongoClient('mongodb://duck_hacker:ssw690@34.228.66.29/ssw690spring2018')
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
        solution = db.solution.find()
    except:
        print('Error retrieving file')

    # solutions = [{'_id':id, 'userid': userid, 'files':files, 'votes':votes, 'solution':solution}
    #              for id, userid, files, votes, solution in solution]
    return solution


def insert_solution(solution, id, files=None):
    """insert solutions into the solution collection"""

    id = randint(0, 9999)
    try:
        db.solution.insert_one(
        {
            '_id': id,
            "userid": 'hannah',
            "files": files,
            "votes": 0,
            "solution": solution
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
            #"exp_id": id,
            "files": files,
            "votes": 0,
            "Experience": experience
        }
        )
    except Exception as e:
        print('Error submitting experience: {}'.format(e))


def increase_count(post_id):
    """increase count of votes by 1"""

    votes=None
    table = db.solution

    try:
        solution = table.find_one({'_id': int(post_id)})
        votes = solution['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes)+1

    try:
        db.solution.update_one(
        {'_id': int(post_id)},
        {"$set":{"votes" : new_vote}
          }
        )
    except Exception as e:
        print('Error updating count: {}'.format(e))


def decrease_count(post_id):
    """decrease count of votes by 1"""
    votes = None
    table = db.solution

    try:
        solution = table.find_one({'_id': int(post_id)})
        votes = solution['votes']

    except Exception as e:
        print('Error finding element : {}'.format(e))

    new_vote = int(votes) - 1
    try:
        db.solution.update_one(
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