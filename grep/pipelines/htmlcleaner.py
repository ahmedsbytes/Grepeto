from HTMLParser import HTMLParser


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
        item['content'] = strip_tags(item['content'])
        item['category'] = strip_tags(item['category'])
        return item