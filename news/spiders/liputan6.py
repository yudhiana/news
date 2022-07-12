# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.lib import remove_tabs, to_number_of_month
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

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[1].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[0],
                                           month,
                                           date_lst[2].replace(',', ''),
                                           date_lst[3])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def parse_detail(self, response):
        item = NewsItem()
        content_lst = response.css(
            '.article-content-body__item-content p::text').getall()
        content = remove_tabs('\n\n'.join(
            content_lst).replace('Baca Juga', ''))
        date_string = response.css(
            'time.read-page--header--author__datetime.updated::text').get()
        item['date_post'] = self.date_parse(date_string)
        item['date_post_local_time'] = date_string
        item['author'] = response.css(
            'span.read-page--header--author__name::text').get()
        item['title'] = response.css(
            'h1.read-page--header--title.entry-title::text').get()
        item['link'] = response.url
        item['content'] = content
        return item
