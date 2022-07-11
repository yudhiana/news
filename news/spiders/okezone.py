# -*- coding: utf-8 -*-
from operator import index
import scrapy
from news.items import NewsItem
from news.lib import remove_tabs, to_number_of_month
from datetime import datetime


class OkezoneSpider(scrapy.Spider):
    name = 'okezone'
    allowed_domains = ['okezone.com']
    index_kanals_id = [1, 2, 11, 12, 13, 14, 16, 613,
                       25, 298, 481, 15, 337, 338, 619, 623, 620]
    base_url = 'https://index.okezone.com/home/channel/'

    def start_requests(self):
        for id in self.index_kanals_id:
            url = self.base_url + str(id)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.list-berita li h4 a::attr(href)'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

        next_page = None
        next_pages = response.css(
            '.pagination-indexs a::attr(href)').getall()
        if next_pages:
            try:
                next_page = next_pages[-2]
            except:
                next_page = next_page[-1]
            pass
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[2].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[4])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def parse_detail(self, response):
        item = NewsItem()
        date_string = response.css('.namerep b::text').get()
        item['date_post'] = self.date_parse(date_string)
        item['date_post_id'] = date_string
        item['author'] = response.css(
            '.namerep ::text').get().replace('\n', '').strip()
        item['title'] = str(response.css('.title h1::text').get()).strip()
        item['link'] = response.url
        item['content'] = remove_tabs('\n\n'.join(
            response.css('#contentx p::text').getall()))
        yield item
