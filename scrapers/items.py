# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    # Данные для таблицы Product
    title = scrapy.Field()
    author = scrapy.Field()
    isbn = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    genre = scrapy.Field()
    
    # Данные для таблицы Offer
    price = scrapy.Field()
    old_price = scrapy.Field()
    url = scrapy.Field()
    website_name = scrapy.Field()
    
    # Дополнительные атрибуты (список словарей)
    attributes = scrapy.Field()