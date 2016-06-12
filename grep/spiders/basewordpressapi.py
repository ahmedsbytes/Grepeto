from grep.extractor.WordpressApiDiggerExtractor import WordpressApiDiggerExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, HtmlResponse
import logging
import json
from grep.items import GrepItem


class BaseWordpressApiSpider(CrawlSpider):

    rules = (
        Rule(WordpressApiDiggerExtractor(), callback='parse_article', follow=True),
    )

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            try:
                body_json = json.loads(response.body_as_unicode())
                response._body = body_json
            except ValueError:
                return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url, callback=self._response_downloaded)
                r.meta.update(rule=n, link_text=link.text)
                yield rule.process_request(r)

    response_json = {}

    def parse_article(self, response):
        self.response_json = response._body
        if type(self.response_json) is not dict:
            self.response_json = json.loads(response._body)
        if 'posts' not in self.response_json or not self.response_json['posts']:
            logging.warning('Not [posts] for ['+response.url+']')
            return

        items = []
        for post in self.response_json['posts']:
            logging.info('Processing post id ['+str(post['ID'])+']')
            item = GrepItem()
            item['url'] = self.getUrl(post)
            item['title'] = self.getTitle(post)
            item['sub_title'] = self.getSubTitle(post)
            item['author'] = self.getAuthor(post)
            item['image'] = self.getImage(post)
            item['time'] = self.getTime(post)
            item['category'] = self.getCats(post)
            item['raw_content'] = item['content'] = self.getContent(post)
            items.append(item)
        return items

    def getUrl(self, post):
        return post['URL']

    def getSubTitle(self, post):
        return post['excerpt']

    def getAuthor(self, post):
        return post['author']['name']

    def getTitle(self, post):
        return post['date']

    def getTime(self, post):
        return post['date']

    def getContent(self, post):
        return post['content']

    def getCats(self, post):
        return post['date']

    def getImage(self, post):
        return  [post['featured_image']]
