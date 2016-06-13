__author__ = 'ahmed'
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from base import BaseSpider


class IclarifiedSpider(BaseSpider):
    name = "iclarified"
    allowed_domains = ["iclarified.com"]
    start_urls = (
        'http://www.iclarified.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('/\d+/[\-0-9a-zA-Z]+$'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('/news(/\d+)?$'), unique=True)),
    )

    xpaths = {
        'title': '//h1/text()',
        'sub_title': '//h1/text()',
        'author': '//span[@itemprop="name"]//text()',
        'image': [
            '//img[@width="640"]//@src',
            '//div[@id="article_body_column_center"]/a/img//@src'
        ],
        'content': '//div[@id="article_body_column_center"]/text()',
        'category': '',
        'time': '//span[@itemprop="datePublished"]//text()'
    }

    def getCats(self):
        return u"Apple"
