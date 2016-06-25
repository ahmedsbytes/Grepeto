import traceback
import sys
import scrapy
import logging
from grep.items import GrepItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BaseSpider(CrawlSpider):
    name = ""
    allowed_domains = []
    start_urls = ()
    rules = ()
    xpaths = {
        'title': '',
        'image': [
            ''
        ],
        'content': '',
        'category': '',
        'sub_title': '',
        'author': '',
        'time': ''
    }

    response = None

    def __init__(self, allowDeep=False, *a, **kw):
        if not allowDeep:
            newRules = []
            for rule in self.rules:
                if rule.callback is not None:
                    rule.follow = False
                    newRules.append(rule)
            self.rules = tuple(newRules)
        super(BaseSpider, self).__init__(*a, **kw)

    def parse_article(self, response):
        self.response = response
        try:
            item = GrepItem()
            item['url'] = self.response.url
            item['title'] = self.getTitle()
            item['sub_title'] = self.getSubTitle()
            item['author'] = self.getAuthor()
            item['image'] = self.getImage()
            item['time'] = self.getTime()
            item['category'] = self.getCats()
            item['raw_content'] = item['content'] = self.getContent()
            return [item]
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            self.log(" Url " + self.response.url + " failed ", logging.ERROR)

    def getSubTitle(self):
        if self.xpaths['sub_title']:
            subtitleSelector = self.getxPath(self.xpaths['sub_title'])
            if subtitleSelector:
                return subtitleSelector[0].strip()
        return ''

    def getAuthor(self):
        return self.getxPath(self.xpaths['author'])[0].strip()

    def getTitle(self):
        return self.getxPath(self.xpaths['title'])[0].strip()

    def getTime(self):
        return self.getxPath(self.xpaths['time'])[0]

    def getContent(self):
        extractedContent = ''
        for singleContent in self.getxPath(self.xpaths['content']):
            extractedContent += singleContent
        return extractedContent

    def getCats(self):
        returnCats = ''
        cats = self.getxPath(self.xpaths['category'])
        for category in cats:
            returnCats += category
        return returnCats.strip()

    def getImage(self):
        returnImages = set()
        for imagePaths in self.xpaths['image']:
            images = self.getxPath(imagePaths)
            for image in images:
                returnImages.add(image.strip())
        return list(returnImages)

    def getxPath(self, selectXpath):
        return self.response.xpath(selectXpath).extract()