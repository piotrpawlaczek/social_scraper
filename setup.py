#!usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='social-scraper',
    author='Piotr Pawlaczek',
    author_email='info@pawlaczek.pl',
    version='0.1',
    packages=find_packages('.'),
    url='https://github.com/piotrpawlaczek/social_scraper',
    description='scalable social scraper',
    long_description='A scalable backend for a web scraper '
                     'initialy makde to retrieve structured content '
                     'from social media like facebook, twitter, linkedin etc',
    install_requires=['scrapy', 'celery', # backend + message queue
                      'flask-restful', # waf
                      'facebook-sdk', 'Twython'], # api clientes
    scripts = ['bin/start_scraper'],
)
