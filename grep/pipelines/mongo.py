__author__ = 'ahmed'
import pymongo
import urlparse
from slugify import slugify
from grep.settings import DB


class MongoPipeline(object):
    collection = None

    def __init__(self):
        client = pymongo.MongoClient()
        db = client[DB['connection']['db']]
        self.collection = db[DB['collection']['articles']]
        self.auto_increment = db[DB['collection']['increment']]
        self.categories = db[DB['collection']['categories']]
        self.websites = db[DB['collection']['websites']]
        pass

    def get_new_increment(self, collection):
        return int(self.auto_increment.find_and_modify(
            query={'_id': collection},
            update={'$inc': {'current_id': 1}},
            fields={'current_id': 1},
            new=True,
            upsert=True
        ).get('current_id'))

    def getCategoryId(self, catName):
        cat = self.categories.find_one({'name': catName})
        if not cat:
            cat = {
                '_id': self.get_new_increment(DB['collection']['categories']),
                'parentId': 0,
                'active': 1,
                'name': catName,
                'slug': slugify(catName)
            }
            self.categories.insert(dict(cat))
        return cat['_id']

    def getArticleId(self, url):
        old_item = self.collection.find_one({'url': url})
        if old_item is None:
            return self.get_new_increment(DB['collection']['articles'])
        else:
            return old_item.get('_id')

    def getWebsiteId(self, item):
        url_parts = urlparse.urlparse(item['url'])
        domain = url_parts[1]
        website = self.websites.find_one({'domain': domain})
        if not website:
            website_link = url_parts[0] + '://' + url_parts[1]
            website = {
                '_id': self.get_new_increment(DB['collection']['websites']),
                'domain': domain,
                'url': website_link,
                'icon': '',
                'description': '',
                'name': ''
            }
            self.websites.insert(dict(website))
        return website['_id']

    def process_item(self, item, spider):
        item['_id'] = self.getArticleId(item['url'])
        item['categoryId'] = self.getCategoryId(item['category'])
        item['websiteId'] = self.getWebsiteId(item)
        self.collection.update({'_id': item['_id']},
                               {'$set': dict(item)}, upsert=True)
        return item
