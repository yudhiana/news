# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem
from news.lib import remove_tabs, to_number_of_month
from datetime import datetime


class SindoSpider(scrapy.Spider):
    name = 'sindo'
    allowed_domains = ['sindonews.com']
    date = datetime.now().strftime('%Y-%m-%d')
    start_urls = ['https://index.sindonews.com/index/0?t={}'.format(date)]

    def parse(self, response):
        pages = self.pages(response)
        if pages:
            for page in pages:
                yield scrapy.Request(url=page, callback=self.parse)

        for href in response.css('.indeks-news .indeks-title a::attr(href)'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

    def pages(self, response):
        result = []
        if re.search('.*index\/0\?t=*', response.url):
            pages = response.css('.pagination li a::attr(data-ci-pagination-page)').getall()[-1]
            pg = 0
            for page in xrange(int(str(pages))):
                pg += 15
                result.append('https://index.sindonews.com/index/0/{}?t={}'.format(pg, self.date))
        return result

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[2].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[5])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date


    def parse_detail(self, response):
        item = NewsItem()
        date_string = response.css('div.article time::text').get()
        item['title'] = response.css('.article h1::text').get()
        item['link'] = response.url
        item['author'] =  response.css('.article .reporter p a::text').get()
        item['date_post'] = self.date_parse(date_string)
        item['date_post_id'] = date_string
        item['content'] = remove_tabs('\n'.join(response.css('.article #content::text').getall()))
        return item

