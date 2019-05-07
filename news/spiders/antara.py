# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem
from bs4 import BeautifulSoup


class AntaraSpider(scrapy.Spider):
    name = 'antara'
    allowed_domains = ['antaranews.com']
    start_urls = ['http://www.antaranews.com/terkini']

    def parse(self, response):
        for href in response.css('.main-content .row article .simple-thumb a ::attr(href)').getall():
            yield scrapy.Request(url=href, callback=self.parse_detail)

        if not re.search('.*terkini\/\d', response.url):
            pages = response.css('ul.pagination li ::text')[-2].get()
            pages = ['{}/{}'.format(self.start_urls[0], x) for x in xrange(2, int(pages) + 1)]
            if pages:
                for page in pages:
                    yield scrapy.Request(url=page, callback=self.parse)


    def parse_detail(self, response):
        item = NewsItem()
        self.clean_content(response)
        author_lst = response.css('p.text-muted.small.mt10::text').getall()[:-1]
        author_lst = [re.sub('[\r\t\n]', '', x).lower() for x in author_lst]
        author_lst = [x.replace('editor:', '').replace('reporter:', '').replace(' ', '') for x in author_lst]
        author_lst = [x for x in author_lst if len(x) != 0]
        item['title'] = response.css('h1.post-title::text').get()
        item['link'] = response.url
        item['date_post_id'] = response.css('span.article-date ::text').get()
        item['author'] = ''.join(author_lst)
        item['content'] = ''.join(response.css('.post-content ::text').getall())
        return item

    def clean_content(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        print(soup.prettify())