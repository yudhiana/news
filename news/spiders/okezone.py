# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem


class OkezoneSpider(scrapy.Spider):
    name = 'okezone'
    allowed_domains = ['okezone.com']
    start_urls = [
        'https://index.okezone.com/bydate/channel/2019/05/03/1',
        'https://index.okezone.com/bydate/channel/2019/05/03/2',
        'https://index.okezone.com/bydate/channel/2019/05/03/11',
        'https://index.okezone.com/bydate/channel/2019/05/03/14',
        'https://index.okezone.com/bydate/channel/2019/05/03/266'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.list-berita li h4 a::attr(href)'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

        next_page = response.css('.pagination-indexs a::attr(href)').getall()[-1]
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = NewsItem()
        item['title'] = str(response.css('.title h1::text').get()).strip()
        item['link'] = response.url
        item['author'] = str(response.css('.namerep ::text').get()).strip().replace('\n', '')
        item['date_post_id'] = str(response.css('.namerep b::text').get()).strip().replace('\n', '')
        item['content'] = ''.join(response.css('#contentx p::text').getall())
        yield item
