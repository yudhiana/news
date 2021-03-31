# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.items import NewsItem
from news.lib import date_parse


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
        item['date_post'] = date_parse(date_str)
        item['date_post_id'] = date_str
        item['author'] = headers.css('.detail__author::text').get()
        item['title'] = headers.css('h1::text').get().strip()
        item['link'] = response.url
        item['content'] = self.content_parse(response)
        
        
        yield item
