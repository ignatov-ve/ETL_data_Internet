# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value
def transform_price(value):
    return int(value)


class LeroymerlenItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor = MapCompose(cleaner_photo))
    charact = scrapy.Field()
    linkes = scrapy.Field(input_processor = MapCompose(transform_price))
    prices = scrapy.Field()
