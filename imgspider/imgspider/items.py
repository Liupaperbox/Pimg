# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    pid = scrapy.Field()
    platform = scrapy.Field()
    orbhash = scrapy.Field()
    imghash = scrapy.Field()
    
