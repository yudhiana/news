# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.lib import remove_tabs, date_parse
from news.items import NewsItem


class JawaposSpider(scrapy.Spider):
    name = 'jawapos'
    allowed_domains = ['jawapos.com']
    date = datetime.now().strftime('%Y-%m-%d')
    base_link = 'https://www.jawapos.com/berita-hari-ini/'
    category = [
        (117874, 'politik'),
        (117885, 'hukum & kriminal'),
        (117887, 'bisnis'),
        (117875, 'nasional'),
        (117888, 'ekomonomy'),
        (117890, 'internasional')
    ]

    def start_requests(self):
        for id in self.category:
            url = '{}?date={}&category={}'.format(
                self.base_link, self.date, id[0])
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for href in response.css('h3.post-list__title'):
            yield scrapy.Request(href.css('a::attr(href)').get(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['date_post'] = self.get_date(response)
        item['date_post_local_time'] = self.get_date_post_local_time(response)
        item['author'] = self.get_author(response)
        item['title'] = self.get_title(response)
        item['link'] = response.url
        item['tags'] = self.get_tags(response)
        item['source'] = self.name
        return item

    def get_content(self, response):
        return self.clean_content(response)

    def clean_content(self, response):
        content_lst = response.css('.content p::text').getall()
        content = '\n\n'.join(content_lst)
        return remove_tabs(content)

    def get_author(self, response):
        author_lst = str(response.css(
            '.content-reporter p::text').get()).split(':')
        author = author_lst[-1].strip()
        return author.title()

    def get_title(self, response):
        return response.css('h1.single-title::text').get().strip()

    def get_date_post_local_time(self, response):
        return response.css('.time::text').get().replace(',', '').strip()

    def get_date(self, response):
        date_id = self.get_date_post_local_time(response)
        if date_id:
            return date_parse(date_id)
        return None

    def get_tags(self, response):
        tags = response.css('.content-tag .tag-list a::text').getall()
        if tags:
            return tags
        return None