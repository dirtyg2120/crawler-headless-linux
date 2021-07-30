# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from wunderground import settings
from scrapy.exceptions import DropItem
import logging

class WundergroundPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    # def process_item(self, item, spider):
    #     self.collection.insert(dict(item))
    #     return item
