# -*- coding: utf-8 -*-
import scrapy
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
        for page in range(2, lastpages+1):
            yield scrapy.Request(self.start_urls[0] + "/" + str(page), callback=self.parse)

        urls = response.css('.media__title a::attr(href)').getall()
        for href in urls:
            yield scrapy.Request(href, callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['date_post'] = self.get_date(response)
        item['date_post_local_time'] = self.get_date_post_local_time(response)
        item['author'] = self.get_author(response)
        item['title'] = self.get_title(response)
        item['link'] = response.url
        item['content'] = self.get_content(response)
        yield item

    def get_content(self, response):
        return self.content_parse(response)

    def content_parse(self, response):
        result = ''
        try:
            result = response.css('.detail__body-text  ::text').getall()
        except:
            pass
        return "".join(result)

    def get_date(self, response):
        date_str = self.get_date_post_local_time(response)
        if date_str:
            return date_parse(date_str)
        return None

    def get_date_post_local_time(self, response):
        headers = response.css('.detail')
        return headers.css('.detail__date::text').get()

    def get_author(self, response):
        headers = response.css('.detail')
        author = headers.css('.detail__author::text').get()
        if author:
            author = str(author).replace('-', '').strip().title()
            return author
        return None

    def get_title(self, response):
        headers = response.css('.detail')
        return headers.css('h1::text').get().strip()
