# -*- coding: utf-8 -*-
import scrapy
import re
from news.lib import remove_tabs, date_parse
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

    def parse_detail(self, response):
        if re.search('.*com\/peristiwa\/.*|.*com\/uang\/.*|.*com\/jakarta\/.*|.*com\/dunia\/.*|.*com\/politik\/.*',
                     response.url):
            item = NewsItem()
            item['date_post'] = self.get_date(response)
            item['date_post_local_time'] = self.get_date_post_local_time(
                response)
            item['author'] = self.get_author(response)
            item['title'] = self.get_title(response)
            item['link'] = response.url
            item['content'] = self.get_content(response)
            return item

    def get_content(self, response):
        return self.clean_content(response)

    def clean_content(self, response):
        content_lst = response.css('.mdk-body-paragraph p ::text').getall()
        if content_lst:
            content = '\n\n'.join(content_lst)
            return remove_tabs(content)
        return None

    def get_title(self, response):
        return response.css('h1::text').get()

    def get_author(self, response):
        return response.css('.reporter a::text').get().title()

    def get_date_post_local_time(self, response):
        return response.css('.date-post::text').get()

    def get_date(self, response):
        date = self.get_date_post_local_time(response)
        if date:
            return date_parse(date)
        return None
