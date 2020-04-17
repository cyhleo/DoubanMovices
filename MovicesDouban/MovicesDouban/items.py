# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    collection = ''
    #片名
    title = scrapy.Field()
    #导演
    directors = scrapy.Field()
    # 主演
    casts = scrapy.Field()
    # 豆瓣评分
    rate = scrapy.Field()
    # 详情页
    movice_url = scrapy.Field()
    # 电影类型
    type = scrapy.Field()