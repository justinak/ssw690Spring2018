"""handle all routing for website. interfaces with Mongocalls.py"""
from flask import Flask, render_template, request, make_response, redirect, url_for
from random import randint
from bson.binary import Binary
import MongoCalls, Experiences_page
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
title = "DuckHacker"
post_questions = {}  # dictionary to contain the question asked to user
App_root = os.path.dirname(os.path.abspath(__file__))  # get file path for files to be uploaded to db


@application.route('/')
def get_questions():
    global post_questions
    questions = MongoCalls.get_question()
    randnum = randint(0, len(questions) - 1)
    post_questions['question'] = questions[randnum]
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)

@application.route('/experience')
def display_experiences():
    experience = Experiences_page.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


@application.route('/question/submit', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        projectpath = request.form['question']
        title = request.form['title']
        topic = request.form['topic']
        MongoCalls.insert_interview(projectpath, title, topic)

    return redirect(url_for('get_questions'))


@application.route('/comment', methods=['POST', 'GET'])
def handle_data():

    if request.method == 'POST':
        answer = request.form['Solution']
        print(post_questions)
        if 'file' not in request.files:
            MongoCalls.insert_solution(answer, post_questions['question']['_id'])
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_solution(answer, post_questions['question']['_id'], files=binfile)

    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'], newcomment = solutions)


@application.route('/question/topic', methods=['POST', 'GET'])
def get_topic_questions():
    questions = None
    if request.method == 'POST':
        print(request.form['topic'])
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

    return render_template('Topics.html', questions=questions)


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


@application.route('/downloads/')
def download_file(filename):
    """Method to handle downloads of files"""
    file = MongoCalls.download_file(filename=filename)
    read_file = make_response(file.read())
    read_file.headers['Content-Type'] = 'application/octet-stream'
    read_file.headers["Content-Disposition"] = "attachment; filename={}".format(filename)

    return read_file


@application.route('/menu', methods=['POST', 'GET'])
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
            return render_template('Topics.html')


@application.route('/question/add')
def display_add_question():
    return render_template('Questions.html')

@application.route('/experience/submit', methods=['POST', 'GET'])
def experience():
    if request.method == 'POST':
        projectpath = request.form['Experience']
        if 'file' not in request.files:
            MongoCalls.insert_experience(projectpath)
            Experiences_page.add_experience(projectpath)
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_experience(projectpath, files=binfile)
                Experiences_page.add_experience(projectpath)

    experience = Experiences_page.get_experience()
    return render_template('Experience.html', title=title, experiences=experience)


@application.route('/voteup/<string:post_id>', methods=['POST'])
def voteUp(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.increase_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


@application.route('/votedown/<string:post_id>', methods=['POST'])
def votedown(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.decrease_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


@application.route('/exvoteup/<string:post_id>', methods=['POST'])
def ex_voteUp(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.increase_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


@application.route('/exvotedown/<string:post_id>', methods=['POST'])
def ex_votedown(post_id):
    """Handle vote ups on click of button for any solution"""
    MongoCalls.decrease_count(post_id)
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title=title, question=post_questions['question']['question'],
                           newcomment=solutions)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.run(debug=True)
