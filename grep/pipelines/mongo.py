__author__ = 'ahmed'
import pymongo
import urlparse
from slugify import slugify
from grep.settings import DB
import logging


class MongoPipeline(object):
    collection = None
    all_websites = all_original_categories = all_categories = None

    def __init__(self):
        client = pymongo.MongoClient()
        db = client[DB['connection']['db']]
        self.collection = db[DB['collection']['articles']]
        self.auto_increment = db[DB['collection']['increment']]
        self.original_categories = db[DB['collection']['original_categories']]
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

    def getCategory(self, catName, domain):
        original_cat = self.original_categories.find_one({'name': catName, 'domain': domain})
        if not original_cat:
            original_cat = {
                '_id': self.get_new_increment(DB['collection']['original_categories']),
                'name': catName,
                'domain': domain,
                'url': '',
                'categoryId': 0
            }
            self.original_categories.insert(original_cat)
        if not original_cat['categoryId']:
            logging.warning('category not mapped yet [' + catName + ']')
        return original_cat

    def getArticleId(self, url):
        old_item = self.collection.find_one({'url': url})
        if old_item is None:
            return self.get_new_increment(DB['collection']['articles'])
        else:
            return old_item.get('_id')

    def getWebsite(self, item):
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
            self.websites.insert(website)
        return website

    def process_item(self, item, spider):
        item['category'] = item['category'].strip()
        item_id = self.getArticleId(item['url'])
        website = self.getWebsite(item)
        original_category = self.getCategory(item['category'], website['domain'])
        if 'category' in original_category:
            item['categoryId'] = original_category['category'].id
        item['originalCategoryId'] = original_category['_id']
        item['websiteId'] = website['_id']
        self.collection.update({'_id': item_id},
                               {'$set': dict(item)}, upsert=True)
        return item
