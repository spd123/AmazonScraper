# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    url  = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    paperback = scrapy.Field()
    hardcover = scrapy.Field()
    kindle_edition = scrapy.Field()

