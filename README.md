[![Build Status](https://travis-ci.org/piotrpawlaczek/social_scraper.svg?branch=master)](https://travis-ci.org/piotrpawlaczek/social_scraper)

Social scraper                                                                                                          
==============

Retrieves user profiles from social networks simulataneusly.
Send `spiders` to the web and gather social content therein!

Install                                                                                                          
-------------                                                                                                           
- python setup.py install
- install celery
- install redis
- edit ```social_scraper/settings.py``` add facebook & twitter `auth` tokens

Test
----                                                                                 
- python run_tests.py

Run
---
- start_scraper

The server is running on port `8080` by default

Celery
------
Be sure to run celery worker before you start:
```
celery -A social_scraper.webapi.celery worker
```

Enjoy                                                                                                               
-----
```
curl -i http://localhost:8080/api/v0.1/users/twitter/sikorskiradek
```
```
curl -i http://localhost:8080/api/v0.1/users/facebook/barackobama
```
you may also access `user_profile` from `js client` or `web browser`

to just run spider, type:
- scrapy runspider twitter -A <username>
- scrapy runspider facebook -A <username>

Deploy
------
Scrapyd allows deploying spiders, starting and stopping them using JSON web service
- pip install scrapyd
- scrapyd-deploy -p social_scraper

Architecture overview
---------------------
![alt tag](http://doc.scrapy.org/en/latest/_images/scrapy_architecture.png)

Job requests (spiders) are initialized from webserver using celery and send to `scrapy` ecosystem

Written with Twisted, a popular event-driven networking framework for Python. Thus, it’s implemented using a non-blocking (aka asynchronous) code for for concurrency.

Todo
----
- Linkedin spider
