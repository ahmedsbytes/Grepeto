# -*- coding: utf-8 -*-
import traceback
import sys
import scrapy
import logging
from grep.items import GrepItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EngadgetSpider(CrawlSpider):
    name = "engadget"
    allowed_domains = ["engadget.com"]
    start_urls = (
        'http://www.engadget.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('/\d+/\d+/\d+/[\-0-9a-zA-Z]+/'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('/[\-0-9a-zA-Z]+/'), unique=True))
    )

    xpaths = {
        'title': '//header/div/div/div/h1/text()',
        'image': '//figure/img[@class="stretch-img"]/@src',
        'content': '//div[@id="page_body"]//div',
        'time': '//p[@itemprop="author creator"]//span[@class="date"]/@data-time'
    }

    response = None

    def parse_article(self, response):
        self.response = response

        try:
            item = GrepItem()
            item['url'] = self.response.url
            item['title'] = self.getxPath(self.xpaths['title'])[0]
            # item['image'] = self.getxPath(self.xpaths['image'])[0]
            # item['time'] = self.getxPath(self.xpaths['time'])[0]
            item['content'] = self.getxPath(self.xpaths['content'])[0]

            return [item]
        except Exception, e:
            traceback.print_exc(file=sys.stderr)
            self.log(" Url failed ", logging.ERROR)

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()
