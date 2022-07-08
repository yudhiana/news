# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.lib import remove_tabs, to_number_of_month
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
            url = '{}?date={}&category={}'.format(self.base_link, self.date, id[0])
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for href in response.css('h3.post-list__title'):
            yield scrapy.Request(href.css('a::attr(href)').get(), callback=self.parse_detail)

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[1].lower())
        date_str = '{}/{}/{} {}'.format(date_lst[0],
                                        month,
                                        date_lst[2].replace(',', '').strip(),
                                        date_lst[3])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def clean_content(self, response):
        content_lst = response.css('.content p::text').getall()
        content = '\n\n'.join(content_lst)
        return remove_tabs(content)

    def parse_detail(self, response):
        item = NewsItem()
        date_string = response.css('.time::text').get().strip()
        author_lst = str(response.css('.content-reporter p::text').get()).split(':')
        author = author_lst[-1].strip()
        item['date_post'] = self.date_parse(date_string)
        item['date_post_id'] = date_string
        item['author'] = author
        item['title'] = response.css('h1.single-title::text').get().strip()
        item['link'] = response.url
        item['content'] = self.clean_content(response)
        return item
