# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from news.items import NewsItem
from news.lib import date_parse
from json import loads


class TribunSpider(scrapy.Spider):
    name = 'tribun'
    allowed_domains = ['tribunnews.com']
    date = datetime.now().strftime('%Y-%m-%d')
    start_urls = [
        'https://www.tribunnews.com/indeks/news'
    ]

    def parse(self, response):
        lastpage = response.css(".paging a::attr(href)").getall()[-1].split('page=')
        pages = int(lastpage[1])
        for page in range(2, pages+1):
            next_page = lastpage[0]+ "page=" + str(page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        urls = response.css('h3 a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url+"?page=all", callback=self.parse_detail)

    def parse_author(self, response):
        author = ''
        scripts = response.css("script")
        for script in scripts:
            script_type = script.css('::attr(type)').get()
            if script_type is not None:
                if 'application/ld+json' in script_type:
                    data = loads(script.css("::text").get().replace("\n","").replace("\t","").strip())
                    if 'author' in data:
                        author = data['author']['name']
        return author

    def parse_detail(self, response):
        content = response.css('.content')
        date_str = content.css('#article time ::text').get().strip()
        item = NewsItem()
        item['date_post'] = date_parse(date_str)
        item['date_post_id'] = date_str
        item['author'] = self.parse_author(response)
        item['title'] = content.css('h1::text').get().strip()
        item['link'] = response.url
        item['content'] = '\n'.join(response.css('.side-article.txt-article p::text').getall())
        yield item