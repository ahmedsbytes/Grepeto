import time
from HTMLParser import HTMLParser
import dateutil.parser as dateparser
import dateparser as dateparser2


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
            try:
                dt = dateparser.parse(item['time'])
                item['time'] = int(time.mktime(dt.timetuple()))
            except ValueError:
                dt = dateparser2.parse(item['time'])
                item['time'] = int(time.mktime(dt.timetuple()))

        item['content'] = strip_tags(item['content'])
        item['category'] = strip_tags(item['category'])
        return item
