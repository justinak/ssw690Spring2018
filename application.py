"""handle all routing for website. interfaces with Mongocalls.py"""
from flask import Flask, render_template, request, make_response, redirect, url_for, Session
from random import randint
from bson.binary import Binary
from Firebase_config import User
import MongoCalls
import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)
title = "DuckHacker"
post_questions = {}  # dictionary to contain the question asked to user
user = None
App_root = os.path.dirname(os.path.abspath(__file__))  # get file path for files to be uploaded
session=Session()

@application.route('/')
def index():
    if 'username' in session.keys():
        return redirect(url_for('get_questions'))
    return render_template('Login.html', title=title)


#############################################################################################################
@application.route('/login',methods=['POST', 'GET'])
def login():
    if request.method =="POST":
        email = request.form['user_email']
        password = request.form['user_pswrd']
        global user
        user = User(email, password)
        token = user.signin()
        #get user name from mongo
        username = MongoCalls.get_specific_user(token)['username']
        global session
        session['username'] = username
        if token != None:
            return redirect(url_for('get_questions'))

    return redirect(url_for('Index'))

##############################################################################################################
@application.route('/logout')
def logout():
    session.pop('username')

    return redirect(url_for('index'))

#############################################################################################################
@application.route('/signup',methods=['POST', 'GET'])
def sign():
    if request.method =="POST":
        email = request.form['user_email']
        password = request.form['user_pswrd']
        username = request.form['user_name']
        global user
        user = User(email, password)
        token = user.create_user()
        session['username'] = username
        print(session)
        if token != None:
            MongoCalls.add_user(token, email, username,
                                'https://pbs.twimg.com/profile_images/676830491383730177/pY-4PfOy_400x400.jpg')
            return redirect(url_for('get_questions'))

    return redirect(url_for('Index'))


################################################################################################################
@application.route('/home')
def user_profile():
    user=MongoCalls.get_userbyid(session['username'])
    return render_template('home.html', user=user)

################################################################################################################
@application.route('/menu', methods=['POST', 'GET'])
def menu_options():
    """Handle clicks of menu options ***still needs to be updated"""
    if request.method == 'POST':
        if request.form['menu'] == 'Experience':
            return redirect(url_for('display_experiences'))
        if request.form['menu'] == 'Profile':
            return redirect(url_for('user_profile'))
        if request.form['menu'] == 'newQuestion':
            return redirect(url_for('display_add_question'))
        if request.form['menu'] == 'Questions':
            return redirect(url_for('get_questions'))
        if request.form['menu'] == 'Topics':
            return redirect(url_for('display_topic'))

################################################################################################
@application.route('/questions')
def get_questions():

    questions = MongoCalls.get_question()
    randnum = randint(0, len(questions) - 1)
    global post_questions
    post_questions['question'] = questions[randnum]
    solutions = MongoCalls.get_solution_by_id(questions[randnum]['_id'])
    return render_template('DuckHacker.html', title=title, question=questions[randnum],
                           newcomment=solutions, username=session['username'])


#######################################################################################################
@application.route('/comment', methods=['POST', 'GET'])
def handle_data():

    if request.method == 'POST':
        answer = request.form['Solution']
        id = request.form['quesid']
        if 'file' not in request.files:
            MongoCalls.insert_solution(answer, id, session['username'])
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_solution(answer, id, session['username'], files=binfile)
        solutions = MongoCalls.get_solution_by_id(id)
        question = MongoCalls.get_specific_ques(id)
        return render_template('DuckHacker.html', title=title, question=question, newcomment=solutions, username=session['username'])

    elif request.method =='GET':
        id=request.form['quesid']
        solutions = MongoCalls.get_solution_by_id(id)
        question = MongoCalls.get_specific_ques(id)
        return render_template('DuckHacker.html', title=title, question=question, newcomment=solutions, username=session['username'])

    # return render_template('DuckHacker.html', title=title, question=question, newcomment=solutions)

#########################################################################################################
@application.route('/question/add')
def display_add_question():
    return render_template('Questions.html', username=session['username'])

########################################################################################################
@application.route('/experience')
def display_experiences():
    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience, username=session['username'])


############################################################################################################
@application.route('/experience/submit', methods=['POST', 'GET'])
def experience():

    if request.method == 'POST':
        projectpath = request.form['Experience']
        if 'file' not in request.files:
            print(session)
            MongoCalls.insert_experience(session['username'], projectpath)
            # Experiences_page.add_experience(projectpath, id)
        else:
            file = request.files['file']
            if file.filename != '':
                binfile = save_file(file)
                MongoCalls.insert_experience(session['username'], projectpath)
                # Experiences_page.add_experience(projectpath, id)

    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience, username=session['username'])


########################################################################################################
@application.route('/question/submit', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        projectpath = request.form['question']
        title = request.form['title']
        topic = request.form['topic']
        MongoCalls.insert_questions(projectpath, title, topic, session['username'])

    return redirect(url_for('get_questions'))


#############################################################################################################
@application.route('/question/topic', methods=['POST', 'GET'])
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

    return render_template('Topics.html', title=title, questions=questions, username=session['username'])


#########################################################################################################
@application.route('/topic/question', methods =['POST', 'GET'])
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
@application.route('/topic')
def display_topic():
    return render_template('Topics.html', title=title, username=session['username'])


#############################################################################################################
@application.route('/vote/<string:post_id>/<string:question_id>', methods=['POST'])
def votesUp(post_id, question_id):
    """Handle vote ups on click of button for any solution"""
    if request.method == "POST":
        if request.form['vote'] == 'voteup':
            print('voteup:', post_id)
            MongoCalls.increase_count(post_id)

        elif request.form['vote'] == 'votedown':
            print('votedown:', post_id)
            MongoCalls.decrease_count(post_id)

    solutions = MongoCalls.get_solution_by_id(question_id)
    question = MongoCalls.get_specific_ques(question_id)
    return render_template('DuckHacker.html', title=title, question=question,
                           newcomment=solutions, username=session['username'])


#########################################################################################################
@application.route('/exvote/<string:post_id>', methods=['POST'])
def exvotesUp(post_id):
    """Handle vote on click of button for any solution"""
    if request.method == "POST":
        if request.form['vote'] == 'voteup':
            print('voteup:', post_id)
            MongoCalls.ex_increase_count(post_id)

        elif request.form['vote'] == 'votedown':
            print('votedown:', post_id)
            MongoCalls.ex_decrease_count(post_id)

    experience = MongoCalls.get_experience()
    return render_template('Experience.html', title=title, experiences=experience, username=session['username'])


########################################################################################################
@application.route('/downloads/')
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


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.secret_key = 'super secret key'
    application.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(application)

application.run(debug=True)
