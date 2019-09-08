# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ImageItem(Item):
    # attention: 将mongodb&mysql的表明做统一设置
    collection = table = 'images'
    
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()
