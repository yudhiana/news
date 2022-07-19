# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.lib import remove_tabs, to_number_of_month, date_parse
from datetime import datetime


class Liputan6Spider(scrapy.Spider):
    name = 'liputan6'
    allowed_domains = ['www.liputan6.com']
    start_urls = [
        'http://www.liputan6.com/news',
        'http://www.liputan6.com/pilpres',
        'http://www.liputan6.com/pileg',
        'http://www.liputan6.com/bisnis'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_link = response.css(
            'aside > header > h4 > a.ui--a.articles--iridescent-list--text-item__title-link')
        for item in item_link:
            yield scrapy.Request(url=item.css('::attr(href)').get(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['date_post'] = self.get_date(response)
        item['date_post_local_time'] = self.get_date_post_local_time(response)
        item['author'] = self.get_author(response)
        item['title'] = self.get_title(response)
        item['link'] = response.url
        item['content'] = self.get_content(response)
        return item

    def get_content(self, response):
        content_lst = response.css(
            '.article-content-body__item-content p::text').getall()
        if content_lst:
            content = remove_tabs('\n\n'.join(
                content_lst).replace('Baca Juga', ''))
            return content
        return None

    def get_title(self, response):
        return response.css('h1.read-page--header--title.entry-title::text').get()

    def get_author(self, response):
        author = response.css(
            'span.read-page--header--author__name::text').get()
        if author:
            return str(author).title()

    def get_date_post_local_time(self, response):
        return response.css('time.read-page--header--author__datetime.updated::text').get()

    def get_date(self, response):
        date = self.get_date_post_local_time(response)
        if date:
            return date_parse(date)
        return None
