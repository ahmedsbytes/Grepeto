__author__ = 'ahmed'

import urlparse
import logging

class ImagePrefixerPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        WebPageUrlParts = urlparse.urlparse(item['url'])
        NewImages = []
        for singleImage in item['image']:
            ImageUrlParts = urlparse.urlparse(singleImage)
            if ImageUrlParts[0]:
                newImage = singleImage
            else:
                if ImageUrlParts[1]:
                    newImage = 'http://' + singleImage
                else:
                    newImage = WebPageUrlParts[0] + '://' + WebPageUrlParts[1] + singleImage
            NewImages.append(newImage)
        item['image'] = NewImages
        return item
