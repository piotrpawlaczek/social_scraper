# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SocialScraperItem(Item):
    id = Field()
    name = Field()
    media = Field()
    photo_uri = Field()
    search_name = Field()
    description = Field()
    popularity_index = Field()
