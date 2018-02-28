from pymongo import MongoClient

client = MongoClient("mongodb://duck_hacker:ssw690@34.228.66.29/videos")

db = client.videos

# print the number of documents in a collection
print(db.get_collection('videos').find_one())