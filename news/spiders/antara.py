# -*- coding: utf-8 -*-
import scrapy
import re
from news.lib import to_number_of_month, remove_tabs, date_parse
from datetime import datetime
from news.items import NewsItem


class AntaraSpider(scrapy.Spider):
    name = 'antara'
    allowed_domains = ['www.antaranews.com']
    start_urls = ['http://www.antaranews.com/terkini']

    def parse(self, response):
        for href in response.css('.main-content .row article .simple-thumb a ::attr(href)').getall():
            yield scrapy.Request(url=href, callback=self.parse_detail)

        if not re.search('.*terkini\/\d', response.url):
            pages = response.css('ul.pagination li ::text')[-2].get()
            pages = ['{}/{}'.format(self.start_urls[0], x)
                     for x in range(2, int(pages) + 1)]
            if pages:
                for page in pages:
                    yield scrapy.Request(url=page, callback=self.parse)

    def clean_author(self, author_list):
        author_lst = [re.sub('[\r\t\n]', '', x).lower() for x in author_list]
        author_lst = [x.lower().replace('editor:', '').
                      replace('pewarta:', '').
                      replace('penerjemah:', '').
                      strip()
                      for x in author_lst]
        author_lst = [x for x in author_lst if len(x) != 0]
        return ' - '.join(author_lst)

    def parse_detail(self, response):
        if re.search('.*www\.antaranews\.com\/berita*', response.url):
            item = NewsItem()
            item['date_post'] = self.get_date(response)
            item['date_post_id'] = self.get_date_post_id(response)
            item['author'] = self.get_author(response)
            item['title'] = self.get_title(response)
            item['link'] = response.url
            item['content'] = self.get_content(response)
            return item

    def get_author(self, response):
        author_lst = response.css(
            'p.text-muted.small.mt10::text').getall()
        if author_lst:
            author_lst = author_lst[:-1]
            return self.clean_author(author_lst).title()
        return None

    def get_title(self, response):
        return response.css('h1.post-title::text').get()

    def get_content(self, response):
        content_lst = response.css('.post-content.clearfix::text').getall()
        if content_lst:
            return remove_tabs(''.join(content_lst))
        return None

    def get_date(self, response):
        date_string = self.get_date_post_id(response)
        if date_string:
            date_string = date_string.strip()
            return date_parse(date_string)
        return None

    def get_date_post_id(self, response):
        date_string = response.css(
            'span.article-date ::text').get()
        if date_string:
            return date_string.strip()
        return None
