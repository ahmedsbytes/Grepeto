__author__ = 'ahmed'
import traceback
import sys
import scrapy
import logging
from grep.items import GrepItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArstechnicaSpider(CrawlSpider):

    #####################
    # # scrappy own vars
    ######################
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'http://techcrunch.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('/[\-0-9a-zA-Z]+/\d+/\d+/[\-0-9a-zA-Z]+/$'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('/[\-0-9a-zA-Z]+$/'), unique=True))
    )


    #######################
    # # my own variables
    #######################
    xpaths = {
        'title': '//header[@class="article-header page-title"]/h1[@class="alpha tweet-title"]//text()',
        'image': '//div[@class="article-entry text"]/img/@src',
        'content': '//div[@class="article-entry text"]//text()',
        'time': '//time[@class="timestamp"]/@datatime'
    }

    response = None

    def parse_article(self, response):
        self.response = response

        try:
            item = GrepItem()
            item['url'] = self.response.url
            item['title'] = self.getxPath(self.xpaths['title'])[0]
            item['image'] = self.getxPath(self.xpaths['image'])[0]
            item['time'] = self.getxPath(self.xpaths['time'])[0]
            content = ''
            for singleContent in self.getxPath(self.xpaths['content']):
                content += singleContent
            item['content'] = content
            return [item]
        except Exception, e:
            traceback.print_exc(file=sys.stderr)
            self.log(" Url failed ", logging.ERROR)

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()