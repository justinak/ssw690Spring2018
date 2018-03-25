from flask import Flask, render_template, request, make_response
from random import randint
from bson.binary import Binary
from pymongo import MongoClient
import MongoCalls
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
client = MongoClient('mongodb://duck_hacker:ssw690@34.228.66.29/ssw690spring2018')
db = client.ssw690spring2018
postquestions = {}
App_root = os.path.dirname(os.path.abspath(__file__))

@application.route('/')
def get_questions():
    questions = MongoCalls.get_question()
    randnum = randint(0, len(questions)-1)
    postquestions['question'] = questions[randnum]
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title="Blah", question=postquestions['question']['Question'], newcomment = solutions)


@application.route('/comment', methods=['POST', 'GET'])
def handle_data():
    target = os.path.join(App_root, 'uploads/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        projectpath = request.form['comments']
        if request.files['input_files']:
            file = request.files['input_files']
            if file.filename:
                destination = "/".join([target, file.filename])
                file.save(destination)
                binfile = convert_binary(destination)
                MongoCalls.insert_solution(projectpath, postquestions['question']['_id'], files=binfile)
        else:
            MongoCalls.insert_solution(projectpath, postquestions['question']['_id'])
        solutions = MongoCalls.get_solution()
        return render_template('DuckHacker.html', title="DuckHacker", question=postquestions['question']['Question'], newcomment = solutions)


def convert_binary(file):
    with open(file,'rb') as fil:
        f = fil.read()
        encoded_file = Binary(f,0)

    return encoded_file

@application.route('/downloads/')
def download_file(filename):
    file = MongoCalls.download_file(filename = filename)
    read_file = make_response(file.read())
    read_file.headers['Content-Type'] = 'application/octet-stream'
    read_file.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return read_file

@application.route('/menu', methods=['POST', 'GET'])
def menu_options():
        if request.method == 'POST':
            if request.form['menu']=='Experience':
                return render_template('Experience.html', title="DuckHacker")
        return render_template('Experience.html', title='DuckHacker')


@application.route('/Experience', methods=['POST', 'GET'])
def experience():
    target = os.path.join(App_root, 'uploads/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        projectpath = request.form['comments']
        if request.files['input_files']:
            file = request.files['input_files']
            if file.filename:
                destination = "/".join([target, file.filename])
                file.save(destination)
                binfile = convert_binary(destination)
                MongoCalls.insert_experience(projectpath, files=binfile)
        else:
            MongoCalls.insert_experience(projectpath)
        solutions = MongoCalls.get_experience()
        return render_template('Experience.html', title="DuckHacker", experiences=solutions)


@application.route('/voteup/<string:post_id>', methods=['POST'])
def voteUp(post_id):
    MongoCalls.increase_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title="Blah", question=postquestions['question']['Question'],
                           newcomment=solutions)


@application.route('/votedown/<string:post_id>', methods=['POST'])
def votedown(post_id):
    MongoCalls.decrease_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title="Blah", question=postquestions['question']['Question'],
                           newcomment=solutions)

# @application.route('/votes')
# def voteUp():
#     print(request.)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()