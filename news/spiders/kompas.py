# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from news.items import NewsItem


class KompasSpider(scrapy.Spider):
    name = 'kompas'
    allowed_domains = ['kompas.com']
    date = datetime.now().strftime('%Y-%m-%d')
    start_urls = ['https://news.kompas.com/search/{}'.format(date)]

    def parse(self, response):
        for href in response.css('.article__list .article__asset a::attr(href)'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

        pages = response.css('.paging__link.paging__link--active::text')[-1].get()
        pg_number = re.sub('.*{}\/([0-9])'.format(self.date), '\g<1>', pages)
        yield response.follow(url='{}/{}'.format(self.start_urls[-1], int(pg_number) + 1))

    def parse_detail(self, response):
        item = NewsItem()
        date = response.css('.read__header .read__time::text').get().replace('Kompas.com - ', '').replace(',', '')
        item['author'] = str(response.css('.read__header .read__author a::text').get()).encode('utf-8')
        item['date_post'] = datetime.strptime(' '.join(date.split(' ')[0:2]), '%d/%m/%Y %H:%M')
        item['date_post_id'] = str(date).encode('utf-8').strip()
        item['content'] = ' '.join(response.css('.read__article .read__content ::text').getall())
        item['link'] = str(response.url).encode('utf-8')
        item['title'] = str(response.css('h1.read__title::text').get()).encode('utf-8')
        yield item
