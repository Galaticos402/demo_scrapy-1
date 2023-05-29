import pymongo
class MongoHelper:
    db = None
    collection = None
    def __init__(self):
        self.connection = pymongo.MongoClient(
            'mongodb+srv://mqd4501:admin@serverlessinstance0.6mgi4.mongodb.net/myFirstDatabase'
            #  "localhost"
            , 27017
        )
        self.db = self.connection["coingecko"]

    def save(self, item, collection_name):
        self.collection = self.db[collection_name]
        self.collection.insert_one(dict(item))

