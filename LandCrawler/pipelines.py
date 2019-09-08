# -*- coding: utf-8 -*-

"""
------------------------------------------------
Description:
    author:  hongzhou_guo@foxmail.com
    date:    2019-09-08
    处理采集到信息的pipline
------------------------------------------------
"""

__author__ = 'hongzhou_guo@foxmail.com'

import time

class LandcrawlerPipeline(object):
    def process_item(self, item, spider):
        self.file.write('{district},{area},{date},{price},{purpose},{supply},{location}\n'.format(**item))
        return item

    def open_spider(self, spider):
        self.file = open('{}.csv'.format(time.time()), 'w', encoding='utf_8_sig')
        self.file.write('district,area,date,price,purpose,supply,location\n')
    
    def close_spider(self, spider):
        self.file.close()