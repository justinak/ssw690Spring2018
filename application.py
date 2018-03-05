from flask import Flask, render_template, request
from random import randint
import stream
import pymongo
from pymongo import MongoClient

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
client = MongoClient('mongodb://duck_hacker:ssw690@34.228.66.29/ssw690spring2018')
db = client.ssw690spring2018
postquestions = {}

@application.route('/')
def getquestions():
    questions = get_question()
    randnum = randint(0, len(questions)-1)
    postquestions['question'] =questions[randnum]
    return render_template('interviewpage.html', title="Blah", question=postquestions['question']['Question'])

@application.route('/comment', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        projectpath = request.form['comments']
        print('@%#^&$*&@(*Success: Data entered')
        insert_solution(projectpath, postquestions['question']['_id'])
        solutions = getsolution()
        return render_template('interviewpage.html', title="Blah", question=postquestions['question']['Question'], newcomment = solutions)


def insert_solution(solution, id):
    db.solution.insert_one(
        {
            "userid": 'hannah',
            "quesid": id,
            "solution": solution
        }
    )

def get_question():

    try:
        questions = db.Interview.find()
    except :
       print('ERROR READING FILE')
    brokendownques = [post for post in questions]
    return brokendownques

def getsolution():
    try:
        solution = db.solution.find()
    except:
        print('Error retrieving file')
    return solution
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()