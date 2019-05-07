# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
from datetime import datetime
from news.items import NewsItem


class TempoSpider(scrapy.Spider):
    name = 'tempo'
    allowed_domains = ['tempo.co']
    date = datetime.now().strftime('%Y/%m/%d')
    start_urls = ['http://tempo.co/indeks/{}'.format(date)]

    def parse(self, response):
        for url in response.css('#article > div.col > section > ul > li  > div > div > a:nth-child(2)::attr(href)'):
            yield scrapy.Request(url=url.get(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        author_lst = response.css('#article #author ::text').getall()
        author_lst = [re.sub('[\r\t\n]', '', x).lower() for x in author_lst]
        author_lst = [x.replace('editor:', '').replace('reporter:', '').replace(' ', '') for x in author_lst]
        author_lst = [x for x in author_lst if len(x) != 0]
        item['link'] = response.url
        item['title'] = response.css('#article h1 ::text').get().replace('\t', '').replace('\r', '').strip()
        item['author'] = ','.join(author_lst)
        item['date_post_id'] = response.css('span#date::text').get()
        item['content'] = ''.join(response.css('#isi ::text').getall())
        yield item
