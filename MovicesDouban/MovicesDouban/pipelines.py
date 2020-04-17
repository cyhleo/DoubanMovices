# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from MovicesDouban.items import DoubanItem
import logging

logger = logging.getLogger(__name__)

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db,):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),

        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[DoubanItem.collection].create_index([('id', pymongo.ASCENDING)])

    def process_item(self, item, spider):
        if isinstance(item, DoubanItem):
            logger.debug('正在向数据库中添加数据')
            self.db[item.collection].update({'title':item.get('title')},{'$set':item},True)
        return item
    def close_spider(self,spider):

        self.client.close()


