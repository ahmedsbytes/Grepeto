# -*- coding: utf-8 -*-
import traceback
import sys
import scrapy
import logging
from grep.items import GrepItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from datetime import datetime
import time

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
        Rule(LinkExtractor(allow=('/(topics\/)?[\-0-9a-zA-Z]+(\/page\/\d+)?\/?/'), unique=True))
    )

    xpaths = {
        'title': '//header/div//h1/text()',
        'image': '//*[@id="page_body"]/div/div/div[1]/div[1]/div/img',
        'content': '//div[@id="page_body"]//div',
        'time': '//div[contains(@class,"t-meta-small@s")]//div[@class="th-meta"]/text()'
    }

    response = None

    def parse_article(self, response):
        self.response = response

        try:
            item = GrepItem()
            item['url'] = self.response.url
            item['title'] = self.getxPath(self.xpaths['title'])[0]
            item['image'] = self.getImage()
            item['time'] = self.getTime()
            item['content'] = self.getxPath(self.xpaths['content'])[0]

            return [item]
        except Exception, e:
            traceback.print_exc(file=sys.stderr)
            self.log(" Url " + self.response.url + " failed ", logging.ERROR)

    def getImage(self):
        Images = self.getxPath(self.xpaths['image'])
        if (len(Images) < 1):
            return ''
        return Images[0]

    def getTime(self):
        time_extracted = self.getxPath(self.xpaths['time'])[0]
        time_extracted = re.sub('in','',time_extracted)
        time_extracted = time_extracted.strip()
        if re.match('\d+h ago',time_extracted):
            return time_extracted;
        else:
            return int(time.mktime(datetime.strptime(time_extracted,'%m.%d.%y').timetuple()))

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()
