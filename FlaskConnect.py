from flask import Flask

# function to print hello world
def hello_world(username="world"):
    return '<p> Hello  %s !</p>' %username

application = Flask(__name__)

application.add_url_rule('/', 'index', (lambda: hello_world()))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:hello_world(username)))

if __name__=='__main__':
    application.debug = True
    application.run()