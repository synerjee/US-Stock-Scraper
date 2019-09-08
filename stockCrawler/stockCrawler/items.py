# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockIndex(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    change = scrapy.Field()
    roc = scrapy.Field()
