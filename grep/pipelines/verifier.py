__author__ = 'ahmed'
import logging


class DataVerifierPipeline(object):

    def process_item(self, item, spider):
        verififcationList = ['title', 'author', 'content', 'image', 'time','category']
        for itemThing in verififcationList:
            if not item[itemThing]:
                logging.warning("url ["+item['url']+"] do not have ["+itemThing+"] ")
                raise Exception("["+itemThing+"] not found")
        return item
