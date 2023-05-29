# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import pymssql

class DemoScrapyPipeline:
    def process_item(self, item, spider):
        return item
class MongoDbPipeline:
    db = None
    connection = None
    def __init__(self):
        self.connection = pymongo.MongoClient(
           'mongodb+srv://mqd4501:admin@serverlessinstance0.6mgi4.mongodb.net/myFirstDatabase'
           #  "localhost"
            ,27017
        )
        self.db = self.connection["coingecko"]
        # self.collection = db["coins"]
    def process_item(self, item, spider):
        collectionName = item.get('Collection')
        self.collection = self.db[collectionName]
        self.collection.insert_one(dict(item))
        return item
