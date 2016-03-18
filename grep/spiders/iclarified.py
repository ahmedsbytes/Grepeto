# -*- coding: utf-8 -*-
import scrapy


class IclarifiedSpider(scrapy.Spider):
    name = "iclarified"
    allowed_domains = ["iclarified.com"]
    start_urls = (
        'http://www.iclarified.com/',
    )

    def parse(self, response):
        pass
