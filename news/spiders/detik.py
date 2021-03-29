# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.items import NewsItem
from news.lib import to_number_of_month


class DetikSpider(scrapy.Spider):
    name = 'detik'
    allowed_domains = ['detik.com']
    start_urls = [
        'https://news.detik.com/indeks/berita',
        'https://news.detik.com/indeks/jawabarat',
        'https://news.detik.com/indeks/jawatengah',
        'https://news.detik.com/indeks/jawatimur',
        'https://news.detik.com/indeks/australiaplus',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pages = response.css('.paging a::attr(href)').getall()
        if len(pages) != 1:
            for page in pages:
                yield scrapy.Request(page, callback=self.parse)

        urls = response.css('#indeks-container > li > article > div')
        for href in urls:
            url = href.css('a::attr(href)').get()
            yield scrapy.Request(url, callback=self.parse_detail)

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
        if response.css('#detikdetailtext'):
            raws = ''.join(response.css('#detikdetailtext::text').getall()).replace('\t', '').replace('\r', '').strip()
        else:
            raws = ''.join(response.css('.detail_text::text').getall()).replace('\t','').replace('\r','').strip()
        return raws

    def parse_detail(self, response):
        item = NewsItem()
        headers = response.css('article > div.jdl')
        date_str = headers.css('.date::text').get()
        item['author'] = headers.css('.author::text').get()
        item['date_post_id'] = headers.css('.date::text').get()
        item['date_post'] = self.date_parse(date_str)
        item['content'] = self.content_parse(response)
        item['link'] = response.url
        item['title'] = headers.css('h1::text').get()
        yield item
