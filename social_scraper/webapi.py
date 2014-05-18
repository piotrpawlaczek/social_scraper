"""
Web interface exposing crawled items
"""
import redis

from flask import Flask
from flask import json
from flask.ext import restful
from flask.ext.restful.representations.json import output_json

from celery import Celery

from twisted.internet import reactor

from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from social_scraper.spiders.twitter import TwitterSpider
from social_scraper.spiders.fb import FacebookSpider

from social_scraper.settings import (API_HOST, API_PORT, API_DEBUG_MODE,
        CELERY_BROKER_URL, CELERY_IMPORTS, CELERY_RESULT_BACKEND,
        CELERYD_MAX_TASKS_PER_CHILD, REDIS_HOST, REDIS_PORT)


# flask app configuration
flask_app = Flask('profile_api')
api = restful.Api(flask_app)

# database setup
flask_app.redis = redis.StrictRedis(REDIS_HOST, port=REDIS_PORT, db=0)

# api output json encoding
output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}

# bind celery to flask app
flask_app.config.update(CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND,
    CELERYD_MAX_TASKS_PER_CHILD=CELERYD_MAX_TASKS_PER_CHILD,
    CELERY_IMPORTS=CELERY_IMPORTS,
)
celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

# Tasks
@celery.task(name='tasks.crawl')
def crawl(username, media):
    """
    Start crawling celery task,
    """
    assert media in ('twitter', 'facebook'), \
        'media :`{}` not supported yet!'.format(media)
    spider = TwitterSpider(username) if media=='twitter' else FacebookSpider(username)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run(installSignalHandlers=0)

def get_json_from_redis(username):
    """ display helper """
    value = flask_app.redis.get('twitter_{}'.format(username))
    if value:
        data = json.loads(value)
        data.pop('id')
        data.pop('search_name')
        if 'description' in data and not str(data['description']).strip():
            data.pop('description')
        return data

# Exposed Resources
class Twitter(restful.Resource):
    def get(self, username):
        data = get_json_from_redis(username)
        if data:
            return data
        crawl.delay(username, 'twitter')
        return 'Processing request'
api.add_resource(Twitter, '/api/v0.1/users/twitter/<string:username>')


class Facebook(restful.Resource):
    def get(self, username):
        data = get_json_from_redis(username)
        if data:
            return data
        crawl.delay(username, media='facebook')
        return 'Processing request'
api.add_resource(Facebook, '/api/v0.1/users/facebook/<string:username>')


if __name__ == "__main__":
  flask_app.debug = API_DEBUG_MODE
  flask_app.run(host=API_HOST, port=int(API_PORT))
