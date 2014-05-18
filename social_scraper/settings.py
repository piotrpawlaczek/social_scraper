# Scrapy settings for social_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'social_scraper'

SPIDER_MODULES = ['social_scraper.spiders']
NEWSPIDER_MODULE = 'social_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'social_scraper (+http(s)://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': None,
}

# PIPELINES
ITEM_PIPELINES = {
    'social_scraper.pipelines.RedisPipeline': 100,
}

# EXTERNAL CREDENTIALS
TWITTER_APP_KEY = ''
TWITTER_TOKEN = ''
FACEBOOK_TOKEN = ''

# REDIS
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# API
API_HOST = '0.0.0.0'
API_PORT = 8080
API_DEBUG_MODE = True

# CELERY
CELERY_BROKER_URL='redis://localhost:6379/2'
CELERY_RESULT_BACKEND='redis://localhost:6379/2'
CELERYD_MAX_TASKS_PER_CHILD=1
CELERY_IMPORTS=['social_scraper.webapi']
