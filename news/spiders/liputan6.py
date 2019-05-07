# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem

class Liputan6Spider(scrapy.Spider):
    name = 'liputan6'
    allowed_domains = ['www.liputan6.com']
    start_urls = [
        'http://www.liputan6.com/news',
        'http://www.liputan6.com/ramadhan',
        'http://www.liputan6.com/pilpres',
        'http://www.liputan6.com/pileg',
        'http://www.liputan6.com/bisnis',
        'http://www.liputan6.com/bola',
        'http://www.liputan6.com/foto',
        'http://www.liputan6.com/techno'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item_link = response.css('aside > header > h4 > a.ui--a.articles--iridescent-list--text-item__title-link')
        for item in item_link:
            yield scrapy.Request(url=item.css('::attr(href)').get(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['title'] = response.css('h1.read-page--header--title.entry-title::text').get()
        item['link'] = response.url
        item['author'] = response.css('span.read-page--header--author__name::text').get()
        item['date_post_id'] = response.css('time.read-page--header--author__datetime.updated::text').get()
        item['content'] = ''.join(response.css('.article-content-body__item-content ::text').getall())
        print item
        return item