from flask import Flask, render_template, request, make_response
from random import randint
from bson.binary import Binary
from pymongo import MongoClient
import MongoCalls

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
post_experience = {}


@application.route('/experience')
def get_experience():
    questions = MongoCalls.get_experience()
    randnum = randint(0, len(questions)-1)
    post_experience['Experience'] = questions[randnum]
    solutions = MongoCalls.get_solution()
    return render_template('DuckHacker.html', title="Blah", question=post_experience['question']['Question'], newcomment = solutions)


@application.route('/Experience', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        projectpath = request.form['comments']
        file = request.files['input_files']
        if file.filename:
            binfile = convert_binary(file)
            MongoCalls.insert_solution(projectpath, file=binfile)
        else:
            MongoCalls.insert_solution(projectpath)
        experience = MongoCalls.get_experience()
        return render_template('Experience.html', title="DuckHacker", experiences = experience)


def convert_binary(file):
    with open(file, "r") as fil:
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


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()