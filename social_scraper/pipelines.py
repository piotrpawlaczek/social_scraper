# Define your item pipelines here
#
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import connection

from twisted.internet.threads import deferToThread
from scrapy.utils.serialize import ScrapyJSONEncoder


class RedisPipeline(object):
    """
    Pushes serialized item into a redis.
    Specific for SocialSpiders
    """

    def __init__(self, server):
        self.server = server
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings(settings)
        return cls(server)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.encoder.encode(item)
        self.server.set(key, data.decode('utf-8'))
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider"""
        return "{}_{}".format(spider.name, item['search_name'])
