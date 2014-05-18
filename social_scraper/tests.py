import unittest

from social_scraper.items import SocialScraperItem
from social_scraper.spiders.twitter import TwitterSpider
from social_scraper.spiders.fb import FacebookSpider


class SocialSpider(object):
    expected_length = 7

    def _test_item_results(self, item):
        self.assertIsInstance(item, SocialScraperItem)
        self.assertIsNotNone(item['id'])
        self.assertIsNotNone(item['name'])
        self.assertIsNotNone(item['photo_uri'])
        self.assertIsNotNone(item['search_name'])
        self.assertIsNotNone(item['popularity_index'])
        self.assertEqual(len(item.keys()), self.expected_length)


class FacebookSpiderTest(SocialSpider, unittest.TestCase):
    def setUp(self):
        self.spider = FacebookSpider()
        self.spider.name = 'facebook-test'
        self.spider.profile = {
                'name': 'fbtestname',
                'picture': {'data': {'url': 'http://test.fb.photo.uri.com'}},
                'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit',
                'friend_count': '1234',
                'id': 98765,
                'search_name': 'fbtestsearch',
        }

    def test_parse_offline(self):
        """
        Test with regards to implementation time api spec
        """
        results = self.spider.parse({})
        self._test_item_results(results)

    def test_parse_online(self):
        """
        Test with regards to current api spec
        """
        self.spider.profile = None
        response = self.spider.api_call('baracobama')
        results = self.spider.parse(response)
        self._test_item_results(results)


class TwitterSpiderTest(SocialSpider, unittest.TestCase):
    def setUp(self):
        self.spider = TwitterSpider()
        self.spider.name = 'twitter-test'
        self.spider.profile = {
                'name': 'twtestname',
                'profile_image_url': {'data': {'url': 'http://test.tw.photo.uri.com'}},
                'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit',
                'followers_count': '4321',
                'id': 456456,
                'search_name': 'twsearchname',
        }

    def test_parse_offline(self):
        """
        Test with regards to implementation time api spec
        """
        results = self.spider.parse({})
        self._test_item_results(results)

    def test_parse_online(self):
        """
        Test with regards to current api spec
        """
        self.spider.profile = None
        response = self.spider.api_call('baracobama')
        results = self.spider.parse(response)
        self._test_item_results(results)


if __name__ == '__main__':
   unittest.main()
