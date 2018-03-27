import stream
import MongoCalls
import _datetime

client = stream.connect('6mrsygzpr525', 's64tas6unkczm5a6dj5qr4w8dgrpgqe2gdy8f8t9cp68ctbezp2fc7exepmkh5ka')
hannah_feed = client.feed('user', 'Hannah')


# add all experiences in mongodb to getstream temporary method
# def add_experiences_from_mongo():
#     experiences = MongoCalls.get_experience()
#     for experience in experiences:
#         hannah_feed.add_activity({'id': experience['_id'], 'actor': experience['userid'], 'tweet': experience['solution'],
#                                     'verb': 'tweet', 'object': 1, 'date': _datetime.datetime.utcnow()})


def add_experience(value):
    hannah_feed.add_activity({'actor': 'Hannah', 'tweet': value, 'verb': 'tweet', 'object': 1})

def get_experience():
    feed = hannah_feed.get()
    print(feed)
    return feed['results']




if __name__ =='__main__':
    #add_experiences_from_mongo()
    get_experience()