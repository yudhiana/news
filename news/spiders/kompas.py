# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from news.items import NewsItem
from news.lib import remove_tabs, date_parse


class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['kompas.com']
    date = datetime.now().strftime('%Y-%m-%d')
    start_urls = ['https://news.kompas.com/search/{}'.format(date)]

    def parse(self, response):
        for href in response.css('.article__list .article__asset a::attr(href)'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

        pages = response.css(
            '.paging__link.paging__link--active::text')[-1].get()
        pg_number = re.sub('.*{}\/([0-9])'.format(self.date), '\g<1>', pages)
        yield response.follow(url='{}/{}'.format(self.start_urls[-1], int(pg_number) + 1))

    def parse_detail(self, response):
        item = NewsItem()
        item['date_post'] = self.get_date(response)
        item['date_post_local_time'] = self.get_date_post_local_time(response)
        item['author'] = self.get_author(response)
        item['title'] = self.get_title(response)
        item['link'] = response.url
        item['content'] = self.get_content(response)
        yield item

    def get_author(self, response):
        author = response.css(
            '.read__header .read__author a::text').get()
        if author is None:
            author = response.css('.read__credit__item a ::text').get()
        return author.title()

    def get_title(self, response):
        return response.css('h1.read__title::text').get()

    def get_content(self, response):
        content_lst = response.css('.read__content p::text').getall()
        if content_lst:
            content = '\n\n'.join(content_lst)
            content = remove_tabs(content)
            return content
        return None

    def get_date_post_local_time(self, response):
        date = response.css('.read__header .read__time::text').get()
        if date:
            return str(date).replace('Kompas.com - ', '').replace(',', '').replace('-', '').strip()

    def get_date(self, response):
        date = self.get_date_post_local_time(response)
        if date:
            return date_parse(date)
        return None
