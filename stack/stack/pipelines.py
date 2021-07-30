# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class StackPipeline:
#     def process_item(self, item, spider):
#         return item

import pymongo

from stack import settings
from scrapy.exceptions import DropItem
import logging

class MongoDBPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]
        

    # def process_item(self, item, spider):
    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem("Missing {0}!".format(data))

    #         if valid:
    #             self.collection.update({'url': item['url']}, dict(item), upsert=True)
    #             logging.msg("Question added to MongoDB database!",
    #                     level=logging.DEBUG, spider=spider)
    #     return item