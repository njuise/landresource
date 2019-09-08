# -*- coding: utf-8 -*-

"""
------------------------------------------------
Description:
    author:  hongzhou_guo@foxmail.com
    date:    2019-09-08
    采集到的中国土地信息对象
------------------------------------------------
"""

__author__ = 'hongzhou_guo@foxmail.com'

import scrapy


class LandcrawlerItem(scrapy.Item):

    area = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    purpose = scrapy.Field()
    supply = scrapy.Field()
    location = scrapy.Field()
    district = scrapy.Field()

