__author__ = 'ahmed'
from slugify import slugify


class SlugifierPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        item['slug'] = slugify(item['title'])
        return item
