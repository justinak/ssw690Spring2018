from pymongo import MongoClient

client = MongoClient("mongodb://duck_hacker:ssw690@34.228.66.29/ssw690spring2018")

db = client.ssw690spring2018

# print the number of documents in a collection
data = db.get_collection('Videos').find()
for d in data:
    print(d) #pylint: disable("print statement used")