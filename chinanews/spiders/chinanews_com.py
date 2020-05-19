# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.utils.project import get_project_settings
from chinanews.items import ChinanewsItem

class ChinanewsComSpider(scrapy.Spider):
    name = 'chinanews_com'
    allowed_domains = ['chinanews.com']

    def __init__(self):
        self.settings = get_project_settings()
        self.begin_date = self.settings['BEGIN_DATE']
        self.end_date = self.settings['END_DATE']
        self.date_list = self.getBetweenDay()

    def start_requests(self):
        for date in self.date_list:
            url = "http://www.chinanews.com/scroll-news" + date + "/news.shtml"
            yield scrapy.Request(url)


    def parse(self, response):
        news_list = response.xpath('//div[@class="content_list"]/ul/li')
        for news in news_list:
            news_url = news.xpath('.//div[@class="dd_bt"]/a/@href').extract_first()
            if isinstance(news_url, str) and not news_url.startswith('http') and not news_url.startswith('/gj'):
                news_url = "http://www.chinanews.com" + news_url
                print(news_url)
                yield scrapy.Request(news_url, callback=self.parse_news)




    def parse_news(self, response):
        item = ChinanewsItem()
        item['news_id'] = response.xpath('//*[@id="newsid"]/@value').extract_first()
        item['news_type'] = response.xpath('//*[@id="newstype"]/@value').extract_first()
        item['news_date'] = response.xpath('//*[@id="newsdate"]/@value').extract_first()
        item['news_title'] = response.xpath('//*[@id="newstitle"]/@value').extract_first()
        item['news_url'] = response.xpath('//*[@id="newsurl"]/@value').extract_first()
        item['news_text'] = response.xpath('//div[@class="left_zw"]//p/text()').extract()
        yield item


    def getBetweenDay(self):
        date_list = []
        begin_date = datetime.datetime.strptime(self.begin_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(self.end_date, "%Y%m%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("/%Y/%m%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)

        return date_list