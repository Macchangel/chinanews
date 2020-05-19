# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from chinanews.items import ChinanewsItem
from chinanews.items import ShChinanewsItem
import datetime
import pymongo


# 清洗数据
class ChinanewsPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ChinanewsItem) or isinstance(item, ShChinanewsItem):
            if item.get('news_text'):
                item['news_text'] = ''.join(item['news_text']).strip().replace(u'\u3000', u'').replace(u'\xa0', u'')
                return item



# 存入MongoDB
class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, ChinanewsItem):
            if item.get('news_date'):
                collection = datetime.datetime.strptime(item['news_date'], "%Y-%m-%d").strftime('%Y%m')    # 将2020-03-03转换为202003，作为表名称
                self.db[collection].insert(dict(item))
                return item
        if isinstance(item, ShChinanewsItem):
            collection = 'Sh'
            self.db[collection].insert(dict(item))
            return item

    def close_spider(self, spider):
        self.client.close()