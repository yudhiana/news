# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from news.items import NewsItem
from news.lib import to_number_of_month, remove_tabs


class TribunSpider(scrapy.Spider):
    name = 'tribun'
    allowed_domains = ['tribunnews.com']
    date = datetime.now().strftime('%Y-%m-%d')
    start_urls = [
        'http://www.tribunnews.com/index-news?date={}'.format(date)
    ]

    def parse(self, response):
        for href in response.xpath('/html/body/div[4]/div[4]/div[1]/div/div[2]/div[2]/ul/li/h3/a/@href'):
            yield scrapy.Request(url=href.get(), callback=self.parse_detail)
        if not re.search('.*&page=.*', response.url):
            paging = response.css('.paging a::attr(href)')
            if paging:
                number_pg = paging[-1].get()
                number_pg = re.sub('.*&page=([0-9]+).*', '\g<1>', number_pg)
                for page in range(2, int(number_pg)):
                    next_page = '{}&page={}'.format(self.start_urls[-1], page)
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
        if re.search(
                '.*news\.com\/nasional.*|.*news\.com\/regional.*|.*news\.com\/internasional.*|.*news\.com\/bisnis.*',
                response.url):
            item = NewsItem()
            date_string = response.css('.content time::text').get()
            item['title'] = response.css('.content h1::text').get()
            item['link'] = response.url
            item['author'] = 'TribunNews'
            item['date_post'] = self.date_parse(date_string)
            item['date_post_id'] = date_string
            item['content'] = remove_tabs('\n\n'.join(response.css('.side-article.txt-article p::text').getall()))
            yield item
