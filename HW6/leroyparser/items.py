# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Compose


def get_id(values):
    pattern = re.compile('(\d+)\/')
    values = int(re.findall(pattern, values)[0])
    return values


def get_link(values):
    pattern = re.compile('<\d+ (.+)>')
    values = re.findall(pattern, values)
    return values


def edit_definitions(values):
    pattern = re.compile('\\n +')
    values = re.sub(pattern, '', values)
    try:
        return float(values)
    except ValueError:
        return values


def change_price(values):
    values = float(values)
    return values


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    photos = scrapy.Field()
    terms = scrapy.Field()
    definitions = scrapy.Field()
    price = scrapy.Field()
    characteristic = scrapy.Field()
    link = scrapy.Field()
