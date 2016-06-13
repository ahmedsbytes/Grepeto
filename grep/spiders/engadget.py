# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re
from datetime import datetime
import time
from base import BaseSpider


class EngadgetSpider(BaseSpider):
    name = "engadget"
    allowed_domains = ["engadget.com"]
    start_urls = (
        'https://www.engadget.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('https://www.engadget.com/\d+/\d+/\d+/[\-0-9a-zA-Z]+/?$'), unique=True),
             callback='parse_article'),
        # rules to allow categories only
        Rule(LinkExtractor(allow=('https://www.engadget.com/(topics/)?[\-0-9a-zA-Z]+(/page/\d+)?/?$'), unique=True)),
    )

    xpaths = {
        'title': '//article/header/div/div/div[2]/h1/text()',
        'sub_title': '//header/div//h2/text()',
        'author': '//header//section//div[@class="t-meta-small@s t-meta@m+"]/a//text()',
        'image': [
            '//*[@id="page_body"]/div/div/div[1]/div[1]/div/img'
        ],
        'content': '//div[@id="page_body"]//div',
        'category': '//header/div//div[@class="th-meta"]/a[@class="th-topic"]/text()',
        'time': '//div[contains(@class,"t-meta-small@s")]//div[@class="th-meta"]/text()'
    }

    def getTime(self):
        time_extracted = self.getxPath(self.xpaths['time'])[0]
        time_extracted = re.sub('in', '', time_extracted)
        time_extracted = time_extracted.strip()
        if re.match('\d+h ago', time_extracted):
            return time_extracted;
        else:
            return int(time.mktime(datetime.strptime(time_extracted, '%m.%d.%y').timetuple()))
