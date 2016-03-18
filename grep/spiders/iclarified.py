# -*- coding: utf-8 -*-
import scrapy
from grep.items import GrepItem
from scrapy.http import Request


class IclarifiedSpider(scrapy.Spider):
    name = "iclarified"
    allowed_domains = ["iclarified.com"]
    start_urls = (
        'http://www.iclarified.com/news/',
    )

    def parse(self, response):
        links = response.xpath('//div[@class="grid_text_title"]//h3//a/@href').extract()

        for link in links:
            url = '{}'.format(''.join(link))
            yield Request(url='http://www.iclarified.com' + url, meta={}, callback=self.parse_item_page)

    def parse_item_page(self, response):
        item = GrepItem()
        item["title"] = response.xpath('//h1/text()'.encode('utf-8')).extract()
        item["url"] = response.xpath('//meta[@property="og:url"]/@content').extract()
        # item["time"] = response.xpath('//h1/text()'.encode('utf-8')).extract()
        # item["image"] = response.xpath('//h1/text()'.encode('utf-8')).extract()
        item["content"] = response.xpath('//div[@id="article_body_column_center"]/text()'.encode('utf-8')).extract()

        return item
