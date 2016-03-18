__author__ = 'ahmed'
from time import gmtime, strftime
import scrapy
from scrapy import log
from grep.items import GrepItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class ArstechnicaSpider(CrawlSpider):

    #####################
    ## scrappy own vars
    ######################
    name = "arstechnica"
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'http://arstechnica.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('/[\-0-9a-zA-Z]+/\d+/\d+/[\-0-9a-zA-Z]+/'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(SgmlLinkExtractor(allow=('/[\-0-9a-zA-Z]+/'), unique=True))
    )


    ## my own variables

    xpaths = {
        'title': '//h1[@itemprop="headline"]//text()',
        'image': '//div[@itemprop="articleBody"]//figure[contains(@class,"intro-image")]//img/@src',
        'content': '//div[@itemprop="articleBody"]//p/text()'
    }

    response = None

    def parse_article(self, response):
        self.response = response

        item = GrepItem()
        item.url = response.url
        item.title = self.getxPath(self.xpaths['title'])[0]
        item.image = self.getxPath(self.xpaths['image'])[0]
        item.content =
        pass

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()

    def log(self, message, level=log.INFO):
        if type(self.response) is scrapy.http.response.html.HtmlResponse:
            message = self.response.url + " " + message
        msg = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + message
        return CrawlSpider.log(self, msg, level)