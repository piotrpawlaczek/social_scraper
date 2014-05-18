from twython import Twython
from social_scraper.items import SocialScraperItem

from social_scraper.settings import TWITTER_APP_KEY, TWITTER_TOKEN
from base import SocialSpider


class TwitterSpider(SocialSpider):
    name = 'twitter'
    start_usernames = ['sikorskiradek']

    def api_call(self, username):
        twitter = Twython(TWITTER_APP_KEY, access_token=TWITTER_TOKEN)
        self.profile = twitter.show_user(screen_name=username)
        self.profile['search_name'] = username
        return twitter._last_call

    def parse(self, response):
        item = SocialScraperItem()
        item['id'] = self.profile['id']
        item['name'] = self.profile['name']
        item['search_name'] = self.profile['search_name']
        item['description'] = self.profile.get('description', '')
        item['photo_uri'] = self.profile['profile_image_url']
        item['popularity_index'] = self.profile['followers_count']
        item['media'] = self.name
        return item
