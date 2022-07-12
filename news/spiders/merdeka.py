# -*- coding: utf-8 -*-
import scrapy
import re
from news.lib import remove_tabs, to_number_of_month
from news.items import NewsItem
from datetime import datetime


class MerdekaSpider(scrapy.Spider):
    name = 'merdeka'
    allowed_domains = ['merdeka.com']
    start_urls = ['https://www.merdeka.com/berita-hari-ini/']

    def parse(self, response):
        for href in response.css('a.mdk-tag-contln-title'):
            detailpage = href.css('::attr(href)').get()
            detailpage = response.urljoin(detailpage)
            yield scrapy.Request(detailpage, callback=self.parse_detail)

        next_page = response.css('span.selected +a::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[2].lower())
        time = date_lst[4]
        time = time if len(time.split(':')) > 2 else '{}:00'.format(time)
        date_str = '{}/{}/{} {}'.format(date_lst[1],
                                        month,
                                        date_lst[3],
                                        time)
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def clean_content(self, response):
        content_lst = response.css('.mdk-body-paragraph p ::text').getall()
        content = '\n\n'.join(content_lst)
        return remove_tabs(content)

    def parse_detail(self, response):
        if re.search('.*com\/peristiwa\/.*|.*com\/uang\/.*|.*com\/jakarta\/.*|.*com\/dunia\/.*|.*com\/politik\/.*',
                     response.url):
            title = response.css('h1::text').get()
            date_string = response.css('.date-post::text').get()
            author = response.css('.reporter a::text').get()
            item = NewsItem()
            item['date_post'] = self.date_parse(date_string)
            item['date_post_local_time'] = date_string
            item['author'] = author
            item['title'] = title
            item['link'] = response.url
            item['content'] = self.clean_content(response)
            return item
