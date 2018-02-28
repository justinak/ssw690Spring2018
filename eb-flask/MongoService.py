from pymongo import MongoClient

client = MongoClient("mongodb://duck_hacker:ssw690@34.228.66.29/ssw690spring2018")

db = client.ssw690spring2018

# print the number of documents in a collection
data = db.get_collection('ssw690spring2018').find_one()

print(data) #pylint: disable("print statement used")