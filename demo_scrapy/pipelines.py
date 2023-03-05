# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class DemoScrapyPipeline:
    def process_item(self, item, spider):
        return item
class MongoDbPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
           'mongodb+srv://mqd4501:admin@serverlessinstance0.6mgi4.mongodb.net/myFirstDatabase?authMechanism=DEFAULT'
            ,27017
        )
        db = connection["crawler_sample"]
        self.collection = db["coins"]
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item