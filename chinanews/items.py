# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_id = scrapy.Field()
    news_type = scrapy.Field()
    news_date = scrapy.Field()
    news_title = scrapy.Field()
    news_text = scrapy.Field()
    news_url = scrapy.Field()
    _id = scrapy.Field()


class ShChinanewsItem(scrapy.Item):
    news_title = scrapy.Field()
    news_text = scrapy.Field()

