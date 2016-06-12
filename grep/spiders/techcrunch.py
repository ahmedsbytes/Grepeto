from grep.spiders.basewordpressapi import BaseWordpressApiSpider


class TechcrunchSpider(BaseWordpressApiSpider):
    name = "techcrunch"
    allowed_domains = ['public-api.wordpress.com']
    start_urls = ['https://public-api.wordpress.com/rest/v1.1/sites/techcrunch.com/posts/?page=1&number=10']