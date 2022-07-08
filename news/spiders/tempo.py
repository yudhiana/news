# -*- coding: utf-8 -*-
import scrapy
import re
from news.lib import to_number_of_month, remove_tabs
from news.items import NewsItem
from datetime import datetime


class TempoSpider(scrapy.Spider):
    name = 'tempo'
    allowed_domains = ['tempo.co']
    date = datetime.now().strftime('%Y/%m/%d')
    start_urls = ['http://tempo.co/indeks/{}'.format(date)]

    def parse(self, response):
        for url in response.css('#article > div.col > section > ul > li  > div > div > a:nth-child(2)::attr(href)'):
            yield scrapy.Request(url=url.get(), callback=self.parse_detail)

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[2].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[4])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def parse_detail(self, response):
        if re.search('.*nasional\.tempo.*|.*bisnis\.tempo.*|.*metro\.tempo.*|.*dunia\.tempo.*', response.url):
            item = NewsItem()
            author_lst = response.css('#article #author ::text').getall()
            author_lst = [re.sub('[\r\t\n]', '', x).lower() for x in author_lst]
            author_lst = [x.replace('editor:', '').replace('reporter:', '').replace(' ', '') for x in author_lst]
            author_lst = [x for x in author_lst if len(x) != 0]
            date_string = response.css('span#date::text').get()
            item['date_post'] = self.date_parse(date_string)
            item['date_post_id'] = date_string
            item['author'] = ' - '.join(author_lst).title()
            item['title'] = response.css('#article h1 ::text').get().replace('\t', '').replace('\r', '').strip()
            item['link'] = response.url
            item['content'] = remove_tabs('\n\n'.join(response.css('#isi p::text').getall()))
            yield item
