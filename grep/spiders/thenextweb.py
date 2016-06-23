__author__ = 'ahmed'
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from base import BaseSpider
import logging


class ThenextwebSpider(BaseSpider):
    name = "thenextweb"
    allowed_domains = ["thenextweb.com"]
    start_urls = (
        'http://thenextweb.com/',
    )

    rules = (
        # # Rules should allow only pages will be craweled
        Rule(LinkExtractor(allow=('[\-0-9a-zA-Z]+/\d+/\d+/\d+/[\-0-9a-zA-Z]+/?$'), unique=True),
             callback='parse_article'),
        # # rules to allow categories only
        Rule(LinkExtractor(allow=('section/[\-0-9a-zA-Z]+$'), unique=True))
    )

    xpaths = {
        'title': '//article/header/h1//text()',
        'image': [
            '//*[contains(@class,"post-featuredImage")]//img/@data-srcset',
            '//*[contains(@class,"post-image")]//img/@data-srcset'
        ],
        'content': '//article/div[contains(@class,"post-body")]/p//text()',
        'category': '//a[contains(@class,"post-section")]//text()',
        'sub_title': '',
        'author': '//a[contains(@class,"post-authorName")]//text()',
        'time': '//header//time[contains(@class,"timeago")]//@datetime'
    }

    response = None

    def getImage(self):
        foundSets = super(ThenextwebSpider, self).getImage()
        if not foundSets:
            return foundSets
        returnImages = set()
        for imageSet in foundSets:
            ImagePath = ''
            for imageCollection in imageSet.split(','):
                lastImageSize = 0
                imageDesc = imageCollection.split(' ')
                if lastImageSize < imageDesc[1]:
                    lastImageSize = imageDesc[1]
                    ImagePath = imageDesc[1]
            if ImagePath:
                returnImages.add(ImagePath)
        return list(returnImages)