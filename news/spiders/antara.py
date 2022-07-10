# -*- coding: utf-8 -*-
import scrapy
import re
from news.lib import to_number_of_month, remove_tabs
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

    def date_parse(self, date_string):
        date_lst = date_string.split(' ')
        month = to_number_of_month(date_lst[2].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[4])
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')

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
            author_lst = response.css(
                'p.text-muted.small.mt10::text').getall()[:-1]
            title = response.css('h1.post-title::text').get()
            link = response.url
            date_string = response.css(
                'span.article-date ::text').get().strip()
            author = self.clean_author(author_lst)
            content_lst = response.css('.post-content.clearfix::text').getall()
            content = remove_tabs(''.join(content_lst))
            item['date_post'] = self.date_parse(date_string)
            item['date_post_id'] = date_string
            item['author'] = author.title()
            item['title'] = title
            item['link'] = link
            item['content'] = content
            return item
