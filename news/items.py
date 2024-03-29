# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date_post_local_time = scrapy.Field()
    date_post = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()
