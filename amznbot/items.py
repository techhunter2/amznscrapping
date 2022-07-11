# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
class AmznbotItem(scrapy.Item):
    # define the fields for your item here like:
    asin = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()
    price = scrapy.Field()
    details = scrapy.Field()
    manufacturer = scrapy.Field()
    color = scrapy.Field()

    
