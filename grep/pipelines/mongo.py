__author__ = 'ahmed'
import pymongo
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
        pass

    def get_new_increment(self, collection):
        return int(self.auto_increment.find_and_modify(
            query={'_id': collection},
            update={'$inc': {'current_id': 1}},
            fields={'current_id': 1},
            new=True,
            upsert=True
        ).get('current_id'))

    def get_existing_item(self, item):
        return self.collection.find_one({'url': item['url']})

    def add_category(self, catName):
        catDict = {
            '_id': self.get_new_increment(DB['collection']['categories']),
            'parentId': 0,
            'active': 1,
            'name': catName,
            'slug': slugify(catName)
        }
        return self.categories.update({'name': catName},
                               {'$set': dict(catDict)}, upsert=True)

    def process_item(self, item, spider):
        self.add_category(item['category'])
        cat = self.categories.find_one({'name': item['category']})
        item['categoryId'] = cat['_id']

        old_item = self.get_existing_item(item)
        if old_item is None:
            item['_id'] = self.get_new_increment(DB['collection']['articles'])
            self.collection.insert(dict(item))
        else:
            item['_id'] = old_item.get('_id')
            self.collection.update({'_id': old_item.get('_id')},
                                   {'$set': dict(item)}, upsert=True)
        return item
