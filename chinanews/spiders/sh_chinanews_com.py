# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from chinanews.items import ShChinanewsItem


class ShChinanewsComSpider(scrapy.Spider):
    name = 'sh_chinanews_com'
    allowed_domains = ['sh.chinanews.com']
    start_urls = ['http://www.sh.chinanews.com/bdrd/index.shtml', 'http://www.sh.chinanews.com/wenhua/index.shtml', 'http://www.sh.chinanews.com/shms/index.shtml', 'http://www.sh.chinanews.com/tiyu/index.shtml', 'http://www.sh.chinanews.com/shishang/index.shtml', 'http://www.sh.chinanews.com/yule/index.shtml', 'http://www.sh.chinanews.com/jinrong/index.shtml', 'http://www.sh.chinanews.com/loushi/index.shtml']


    def parse(self, response):
        news_list = response.xpath('//ul[@class="branch_list_ul paging"]/li')
        for news in news_list:
            news_url = news.xpath('.//div[@class="con_title"]/a/@href').extract_first()
            if isinstance(news_url, str):
                news_url = "http://www.sh.chinanews.com" + news_url
                yield scrapy.Request(news_url, callback=self.parse_news)





    def parse_news(self, response):
        item = ShChinanewsItem()
        item['news_title'] = response.xpath('//div[@class="cms-news-article-title"]/span/text()').extract_first()
        item['news_text'] = response.xpath('//div[@class="cms-news-article-content-blocknew"]/p/text()').extract()
        yield item