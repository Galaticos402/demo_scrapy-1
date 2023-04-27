# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import pymssql
import pyodbc

class DemoScrapyPipeline:
    def process_item(self, item, spider):
        return item
class MongoDbPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
           # 'mongodb+srv://mqd4501:admin@serverlessinstance0.6mgi4.mongodb.net/myFirstDatabase?authMechanism=DEFAULT'
            "localhost"
            ,27017
        )
        db = connection["crawler_sample"]
        self.collection = db["coins"]
    def process_item(self, item, spider):
        print("Pipeline called")
        self.collection.insert_one(dict(item))
        return item

class MSSQLDbPipeline:
    def __init__(self):
        self.conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', server='tcp:chainblade.database.windows.net,1433', user='mquan', password='wuandmSE150021@', database='ChainBlade')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("INSERT INTO Coin(name, code, price) VALUES (?, ?, ?)",
                                (item['name'], item['code'], item['price']))
            self.conn.commit()
        except pymssql.Error as e:
            print("error")
        return item