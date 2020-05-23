# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrappingquoteItem(scrapy.Item):
    # define the fields for your item here like:
    # 5.1) Save extracted data to items container
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()