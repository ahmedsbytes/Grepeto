__author__ = 'ahmed'
import pymongo


class MongoPipeline(object):
    collection = None
    safe = False

    def __init__(self):
        client = pymongo.MongoClient()
        db = client['project_grep']
        self.collection = db['crawled_articles']
        pass


    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item