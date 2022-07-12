# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from news.lib import remove_tabs, to_number_of_month
from news.items import NewsItem


class SuaraSpider(scrapy.Spider):
    name = 'suara'
    allowed_domains = ['suara.com']
    year = datetime.now().year
    base_link = 'https://www.suara.com/indeks/terkini/'
    categories = ['news', 'bisnis', 'banten',
                  'jabar', 'jateng', 'jatim', 'jogja']

    def start_requests(self):
        for category in self.categories:
            url = '{}{}/{}'.format(self.base_link, category, self.year)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        links_detail = response.css('h4 a.ellipsis2')
        if len(links_detail) != 0:
            for href in links_detail:
                url = href.css('::attr(href)').get()
                yield scrapy.Request(url+'?page=all', callback=self.parse_detail)

            next_page = response.css('.pagination li.active +li')
            if next_page:
                next_page = next_page.css('::attr(href)').get()
                yield scrapy.Request(next_page, callback=self.parse)

    def clean_content(self, response):
        content_lst = response.css('.content-article p ::text').getall()
        content = '\n\n'.join(content_lst)
        return remove_tabs(content)

    def date_parse(self, date_string):
        date_lst = str(date_string).strip().split(' ')
        month = to_number_of_month(date_lst[2].lower())
        date_str = '{}/{}/{} {}:00'.format(date_lst[1],
                                           month,
                                           date_lst[3],
                                           date_lst[5])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        return date

    def parse_detail(self, response):
        if re.search('.*suara\.com\/news\/.*|.*suara\.com\/bisnis\/.*|.*suara\.com\/dpr\/.*|.*suara\.com\/read\/.*',
                     response.url):
            item = NewsItem()
            item['date_post'] = self.date_parse(self.get_date(response))
            item['date_post_local_time'] = self.get_date(response)
            item['author'] = self.get_author(response)
            item['title'] = self.get_title(response)
            item['link'] = response.url
            item['content'] = self.get_content(response)
            return item

    def get_date(self, response):
        date_string = response.css('.dateDetail .fr time::text').get()
        if date_string:
            return date_string
        else:
            date_obj = response.css('.detail--info span::text').getall()
            if date_obj:
                obj = date_obj[-1]
                if obj:
                    return obj.strip()
        return None

    def get_author(self, response):
        author = response.css('.dateDetail .fl author::text').get()
        if not author:
            author = response.css('.detail--info span::text').get()
        return author

    def get_content(self, response):
        content = self.clean_content(response)
        if not content:
            content_lst = response.css('.detail--content p::text').getall()
            if content_lst:
                content = '\n\n'.join(content_lst)
                content = remove_tabs(content)
        return content

    def get_title(self, response):
        title = response.css('.title h1::text').get()
        if not title:
            title = response.css('.detail h1::text').get()
        return title
