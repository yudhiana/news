# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem
from news.lib import remove_tabs, to_number_of_month, utc_to_id_month
from datetime import datetime


class RepublikaSpider(scrapy.Spider):
    name = 'republika'
    allowed_domains = ['republika.co.id']
    date = datetime.now().strftime('%Y/%m/%d')
    start_urls = ['https://www.republika.co.id/index/{}'.format(date)]

    def parse(self, response):
        links = response.css('.txt_subkanal h2')
        if len(links) != 0:
            for href in links:
                url_page = href.css('a::attr(href)').get()
                yield scrapy.Request(url_page, callback=self.parse_detail)

            next_page = response.css('nav a::attr(href)').getall()
            if next_page:
                yield scrapy.Request(next_page[-1], callback=self.parse)

    def clean_author(self, author_str):
        author_lst = str(author_str).strip().replace(
            '\n', '').strip().split(':')
        author_lst = [x.replace('Red', '').replace(
            'Rep', '').replace('/', '').strip() for x in author_lst]
        author_lst = [x for x in author_lst if len(x) != 0]
        author = ' - '.join(author_lst) if len(
            author_lst) > 1 else ''.join(author_lst)
        return author

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = utc_to_id_month(date_lst[2].lower())
        month = to_number_of_month(month)
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[4])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def clean_content(self, response):
        content_lst = response.css('.artikel  p ::text').getall()
        if content_lst:
            content = remove_tabs('\n'.join(content_lst))
        else:
            content_lst = response.css('[itemprop="articleBody"] p::text').getall()
            content = remove_tabs('\n'.join(content_lst))
        return content

    def parse_detail(self, response):
        title = response.css('.wrap_detail_set h1::text').get()
        date_string = response.css('.date_detail p::text').get()
        date_string = re.sub('[ ]+', ' ', date_string)
        author = response.css('.by > span > p::text').get()
        author = self.clean_author(author)
        link = response.url
        item = NewsItem()
        item['date_post'] = self.date_parse(date_string)
        item['date_post_id'] = date_string
        item['author'] = author
        item['title'] = title
        item['link'] = link
        item['content'] = self.clean_content(response)
        return item
