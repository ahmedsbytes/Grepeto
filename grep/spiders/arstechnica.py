__author__ = 'ahmed'
from base import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArstechnicaSpider(BaseSpider):
    name = "arstechnica"
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'http://arstechnica.com/',
    )
    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('http://arstechnica.com/([^/\.]+)/\d+/\d+/([^/\.]+)/?$'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('http://arstechnica.com/([^/\.]+)+(/page/\d+)?/?$'), unique=True))
    )


    xpaths = {
        'title': '//h1[@itemprop="headline"]//text()',
        'image': [
            '//div[@itemprop="articleBody"]//figure[contains(@class,"intro-image")]//img/@src',
            '//div[@itemprop="articleBody"]//figure[contains(@class,"image")]//img/@src'
        ],
        'content': '//div[@itemprop="articleBody"]//p/text()',
        'category' : '//h1[@id="archive-head"]//span',
        'time': '//p[@itemprop="author creator"]//span[@class="date"]/@data-time'
    }