__author__ = 'ahmed'
import traceback
import sys
import scrapy
import logging
from grep.items import GrepItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IclarifiedSpider(CrawlSpider):

    #####################
    # # scrappy own vars
    ######################
    name = "iclarified"
    allowed_domains = ["iclarified.com"]
    start_urls = (
        'http://www.iclarified.com/news/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('\/\d+\/[\-0-9a-zA-Z]+$'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('news\/\d+'), unique=True))
    )


    #######################
    # # my own variables
    #######################
    xpaths = {
        'title': '//h1/text()',
        'image': '//img[@width="640"]//@src',
        'content': '//div[@id="article_body_column_center"]/text()',
        'time': '//span[@itemprop="datePublished"]//text()'
    }

    response = None

    def parse_article(self, response):
        self.response = response

        try:
            item = GrepItem()
            item['url'] = self.response.url
            item['title'] = self.getxPath(self.xpaths['title'])[0]
            item['image'] = self.getImage()
            item['time'] = self.getxPath(self.xpaths['time'])[0]
            content = ''
            for singleContent in self.getxPath(self.xpaths['content']):
                content += singleContent
            item['raw_content'] = item['content'] = content
            return [item]
        except Exception, e:
            traceback.print_exc(file=sys.stderr)
            self.log(" Url " + self.response.url + " failed ", logging.ERROR)

    def getImage(self):
        Images = self.getxPath(self.xpaths['image'])
        if (len(Images) < 1):
            return ''
        return Images[0]

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()