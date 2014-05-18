import facebook

from social_scraper.settings import FACEBOOK_TOKEN
from social_scraper.items import SocialScraperItem

from base import SocialSpider


class FacebookSpider(SocialSpider):
    name = 'facebook'
    start_usernames = ['baracobama']

    def api_call(self, username):
        api = facebook.GraphAPI(FACEBOOK_TOKEN)
        args = {'fields' : 'id,name,picture,about'}
        profile = api.get_object(username, **args)
        profile.update(
            api.fql(
                'SELECT friend_count FROM user WHERE uid = {}'\
                .format(profile['id'])
            )[0]
        )
        self.profile = profile
        self.profile['search_name'] = username
        return {
            'status_code': 200,
            'url': 'https://graph.facebook.com/{}'.format(username),
            'content': repr(profile)
        }

    def parse(self, response):
        item = SocialScraperItem()
        item['name'] = self.profile['name']
        item['photo_uri'] = self.profile['picture']['data']['url']
        item['description'] = self.profile.get('description')
        item['search_name'] = self.profile['search_name']
        item['popularity_index'] = self.profile['friend_count']
        item['media'] = self.name
        item['id'] = int(self.profile['id'])
        return item
