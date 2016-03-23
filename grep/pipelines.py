# -*- coding: utf-8 -*-
import time
import dateutil.parser as dateparser
from HTMLParser import HTMLParser


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class CleanerPipeline(object):
    def process_item(self, item, spider):
        if not item['time'].isdigit():
            dt = dateparser.parse(item['time'])
            item['time'] = int(time.mktime(dt.timetuple()))

        item['content'] = strip_tags(item['content'])
        return item
