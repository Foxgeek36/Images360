# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ImageItem(Item):
    # attention: 将mongodb&mysql的数据存储做统一设置/ 此处是对数据库及mysql表名做设置
    collection = table = 'images'
    
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()
