# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.items import NewsItem


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

    def to_number_of_month(self, month_str):
        month_lst = [('januari', '01'), ('februari', '02'), ('maret', '03'), ('april', '04'),
                     ('mei', '05'), ('juni', '06'), ('juli', '07'), ('agustus', '08'),
                     ('september', '09'), ('oktober', '10'), ('november', '11'), ('december', '12')]
        month = [x[1] for x in month_lst if x[0] == month_str]
        return ''.join(month)

    def date_parse(self, date_string):
        date_lst = date_string.split(' ')
        if len(date_lst) != 3:
            date_lst = date_lst[1:-1]
            date_str = '{}/{}/{} {}'.format(date_lst[0],
                                            self.to_number_of_month(date_lst[1].lower()),
                                            date_lst[2].replace(',', ''), date_lst[3])
            date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        else:
            date_lst = date_lst[:-1]
            date_str = ' '.join(date_lst)
            date = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
        return date

    def content_parse(self, response):
        if response.css('#detikdetailtext'):
            raws = response.css('#detikdetailtext ::text').getall()
        else:
            raws = response.css('.detail_text ::text').getall()
        return ' '.join(raws).strip()

    def parse_detail(self, response):
        item = NewsItem()
        headers = response.css('article > div.jdl')
        date_str = headers.css('.date::text').get()
        item['author'] = headers.css('.author::text').get().encode('utf-8')
        item['date_post_id'] = headers.css('.date::text').get().encode('utf-8')
        item['date_post'] = self.date_parse(date_str)
        item['content'] = self.content_parse(response)
        item['link'] = response.url.encode('utf-8')
        item['title'] = headers.css('h1::text').get().encode('utf-8')
        yield item
