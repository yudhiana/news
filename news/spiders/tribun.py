# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from news.items import NewsItem


class TribunSpider(scrapy.Spider):
    name = 'tribun'
    allowed_domains = ['tribunnews.com']
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    start_urls = [
        'http://www.tribunnews.com/index-news/all?date={}-{}-{}'.format(year, month, day),
    ]
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,en-CA;q=0.7,en-ZA;q=0.6,en-AU;q=0.5,en-NZ;q=0.4,id;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.tribunnews.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            print url
            yield scrapy.Request(url=url, headers=self.header)

    def parse(self, response):
        for href in response.xpath('/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/ul/li/h3/a/@href'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = NewsItem()
        item['title'] = response.css('.content h1::text').get()
        item['link'] = response.url
        item['date_post_id'] = response.css('.content time::text').get()
        item['content'] = ''.join(response.css('.side-article.txt-article ::text').getall())
        yield item

