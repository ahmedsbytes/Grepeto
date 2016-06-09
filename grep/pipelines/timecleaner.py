import dateutil.parser as dateparser
import dateparser as dateparser2
import time


class DateCleanerPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item['time'], int) and not item['time'].isdigit():
            try:
                dt = dateparser.parse(item['time'])
                item['time'] = int(time.mktime(dt.timetuple()))
            except ValueError:
                dt = dateparser2.parse(item['time'])
                item['time'] = int(time.mktime(dt.timetuple()))
        else:
            item['time'] = int(item['time'])
        return item
