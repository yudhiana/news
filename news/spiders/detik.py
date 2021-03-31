# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.items import NewsItem
from news.lib import to_number_of_month


class DetikSpider(scrapy.Spider):
    name = 'detik'
    allowed_domains = ['detik.com']
    start_urls = [
        'https://news.detik.com/indeks'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pages = response.css('.pagination a::attr(href)').getall()
        lastpages = int(pages[-2].split("/")[-1])
        for page in range(2,lastpages+1):
           yield scrapy.Request(self.start_urls[0]+ "/" + str(page), callback=self.parse)

        urls = response.css('.media__title a::attr(href)').getall()
        for href in urls:
            yield scrapy.Request(href, callback=self.parse_detail)

    def date_parse(self, date_string):
        date_lst = date_string.split(' ')
        if len(date_lst) != 3:
            date_lst = date_lst[1:-1]
            date_str = '{}/{}/{} {}:00'.format(date_lst[0],
                                            to_number_of_month(date_lst[1].lower()),
                                            date_lst[2].replace(',', ''), date_lst[3])
            date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        else:
            date_lst = date_lst[:-1]
            date_str = ' '.join(date_lst)
            date = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
        return date

    def content_parse(self, response):
        result = ''
        try:
            result = response.css('.detail__body-text  ::text').getall()

        except:
            pass
        return "".join(result)

    def parse_detail(self, response):
        item = NewsItem()
        headers = response.css('.detail')
        date_str = headers.css('.detail__date::text').get()
        item['author'] = headers.css('.detail__author::text').get()
        item['date_post_id'] = date_str
        item['date_post'] = self.date_parse(date_str)
        item['content'] = self.content_parse(response)
        item['link'] = response.url
        item['title'] = headers.css('h1::text').get().strip()
        yield item
