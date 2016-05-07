__author__ = 'ahmed'
import pymongo


class MongoPipeline(object):
    collection = None

    def __init__(self):
        client = pymongo.MongoClient()
        db = client['project_grep']
        self.collection = db['crawled_articles']
        self.auto_increment = db['doctrine_increment_ids']
        pass

    def get_new_increment(self):
        return int(self.auto_increment.find_and_modify(
            query={'_id': 'GeneratedContent'},
            update={'$inc': {'current_id': 1}},
            fields={'current_id': 1},
            new=True,
            upsert=True
        ).get('current_id'))

    def get_existing_item(self, item):
        return self.collection.find_one({'url': item['url']})

    def process_item(self, item, spider):
        old_item = self.get_existing_item(item)
        if old_item is None:
            item['_id'] = self.get_new_increment()
            self.collection.insert(dict(item))
        else:
            item['_id'] = old_item.get('_id')
            self.collection.update({'_id': old_item.get('_id')},
                                   {'$set': dict(item)}, upsert=True)
        return item
