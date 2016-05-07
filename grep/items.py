# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GrepItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    slug = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    image = scrapy.Field()
    content = scrapy.Field()
    summary = scrapy.Field()
    pass
