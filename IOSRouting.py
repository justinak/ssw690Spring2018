import stream
from flask import Flask
from random import randint
import _datetime

client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
application = Flask(__name__)

class user:
    def __init__(self, username):
        self.name = username
        self.feed = client.feed('user', username)
        self.id = randint(0, 9999)

    def add_experience(self, value, verb):
        self.feed.add_activity({'actor': self.name, 'tweet': value, 'verb': verb, 'foreignid': self.id,
                                'date':_datetime.datetime.utcnow()})

    def get_feed(self):
        feed = self.feed.get()
        return feed['results']

    def follows(self, fuser):
        self.feed.follow('user', fuser)

    def unfollows(self, fuser):
        self.feed.unfollow('user', fuser)

user_hannah = user('Hannah')


application.route("/experience/post")
def add_experience(value):
    user_hannah.add_activity(value=value, verb='tweet')


application.route('/experience/feed')
def get_experience():
    return user_hannah.get_feed()




if __name__ =='__main__':
    #add_experiences_from_mongo()
    get_experience()