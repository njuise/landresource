# -*- coding: utf-8 -*-

"""
------------------------------------------------
Description:
    author:  hongzhou_guo@foxmail.com
    date:    2019-09-08
    采集中国土地市场网信息
------------------------------------------------
"""

__author__ = 'hongzhou_guo@foxmail.com'

import scrapy
import json
import re
from LandCrawler.items import LandcrawlerItem


class landSpider(scrapy.Spider):
    name = 'land'
    # allowed_domains = ['landchina.com']

    def __init__(self, startDate=None, endDate=None):
        
        self.startDate = startDate
        self.endDate = endDate

        self.headers = {
            'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Cookie': "security_session_verify=7dce296d3684029ab512d20613f8762f; security_session_high_verify=3c77bd1b34702a62fd1148316fe81255; ASP.NET_SessionId=u2vumwqqiwv5hbb4fzjentec; Hm_lvt_83853859c7247c5b03b527894622d3fa=1567604261; Hm_lvt_83853859c7247c5b03b527894622d3fa=1567604261; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1567604703; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1567607398",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            'Cache-Control': "no-cache",
            'Host': "www.landchina.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': 'keep-alive'
        }


        # 有三个参数，startDate, endDate, page
        self.payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n/wEPDwUJNjkzNzgyNTU4D2QWAmYPZBYIZg9kFgICAQ9kFgJmDxYCHgdWaXNpYmxlaGQCAQ9kFgICAQ8WAh4Fc3R5bGUFIEJBQ0tHUk9VTkQtQ09MT1I6I2YzZjVmNztDT0xPUjo7ZAICD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHgRUZXh0ZWRkAgEPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFhwFDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6O0JBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3dfc3lfamhnZ18wMDAuZ2lmKTseBmhlaWdodAUBMxYCZg9kFgICAQ9kFgJmDw8WAh8CZWRkAgIPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHwJlZGQCAg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAICD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCAgEPZBYCZg8WBB8BBYYBQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjtCQUNLR1JPVU5ELUlNQUdFOnVybChodHRwOi8vd3d3LmxhbmRjaGluYS5jb20vVXNlci9kZWZhdWx0L1VwbG9hZC9zeXNGcmFtZUltZy94X3Rkc2N3X3p5X2pnZ2dfMDEuZ2lmKTsfAwUCNDYWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIBD2QWAmYPZBYCZg9kFgJmD2QWAgIBD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIDD2QWAgIDDxYEHglpbm5lcmh0bWwF/AY8cCBhbGlnbj0iY2VudGVyIj48c3BhbiBzdHlsZT0iZm9udC1zaXplOiB4LXNtYWxsIj4mbmJzcDs8YnIgLz4NCiZuYnNwOzxhIHRhcmdldD0iX3NlbGYiIGhyZWY9Imh0dHBzOi8vd3d3LmxhbmRjaGluYS5jb20vIj48aW1nIGJvcmRlcj0iMCIgYWx0PSIiIHdpZHRoPSIyNjAiIGhlaWdodD0iNjEiIHNyYz0iL1VzZXIvZGVmYXVsdC9VcGxvYWQvZmNrL2ltYWdlL3Rkc2N3X2xvZ2UucG5nIiAvPjwvYT4mbmJzcDs8YnIgLz4NCiZuYnNwOzxzcGFuIHN0eWxlPSJjb2xvcjogI2ZmZmZmZiI+Q29weXJpZ2h0IDIwMDgtMjAxOSBEUkNuZXQuIEFsbCBSaWdodHMgUmVzZXJ2ZWQmbmJzcDsmbmJzcDsmbmJzcDsgPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPg0KdmFyIF9iZGhtUHJvdG9jb2wgPSAoKCJodHRwczoiID09IGRvY3VtZW50LmxvY2F0aW9uLnByb3RvY29sKSA/ICIgaHR0cHM6Ly8iIDogIiBodHRwczovLyIpOw0KZG9jdW1lbnQud3JpdGUodW5lc2NhcGUoIiUzQ3NjcmlwdCBzcmM9JyIgKyBfYmRobVByb3RvY29sICsgImhtLmJhaWR1LmNvbS9oLmpzJTNGODM4NTM4NTljNzI0N2M1YjAzYjUyNzg5NDYyMmQzZmEnIHR5cGU9J3RleHQvamF2YXNjcmlwdCclM0UlM0Mvc2NyaXB0JTNFIikpOw0KPC9zY3JpcHQ+Jm5ic3A7PGJyIC8+DQrniYjmnYPmiYDmnIkmbmJzcDsg5Lit5Zu95Zyf5Zyw5biC5Zy6572RJm5ic3A7Jm5ic3A75oqA5pyv5pSv5oyBOua1meaxn+iHu+WWhOenkeaKgOiCoeS7veaciemZkOWFrOWPuCZuYnNwOzxiciAvPg0K5aSH5qGI5Y+3OiDkuqxJQ1DlpIcwOTA3NDk5MuWPtyDkuqzlhaznvZHlronlpIcxMTAxMDIwMDA2NjYoMikmbmJzcDs8YnIgLz4NCjwvc3Bhbj4mbmJzcDsmbmJzcDsmbmJzcDs8YnIgLz4NCiZuYnNwOzwvc3Bhbj48L3A+HwEFZEJBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3cyMDEzX3l3XzEuanBnKTtkZM3NvnlXlCHsxkc6av00AJnK3vbhmjQCCXm5QkCZwr58\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTVALIDATION\"\r\n\r\n/wEdAAIo20rirRFW2+eFhO6+Mw9qCeA4P5qp+tM6YGffBqgTjTZh/IuwdhzpiegZclaPF5waXsY9AwQQV7PLcCma+lPB\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hidComName\"\r\n\r\ndefault\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QueryConditionItem\"\r\n\r\n9f2c3acd-0256-4da2-a659-6949c4671a2a\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QuerySortItemList\"\r\n\r\n282:False\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QuerySubmitConditionData\"\r\n\r\n9f2c3acd-0256-4da2-a659-6949c4671a2a:{startDate}~{endDate}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QuerySubmitOrderData\"\r\n\r\n282:False\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_RowButtonActionControl\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QuerySubmitPagerData\"\r\n\r\n{page}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"TAB_QuerySubmitSortData\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"

        self.basic_url = 'https://www.landchina.com/'
        self.url = 'https://www.landchina.com/default.aspx?tabid=263&ComName=default/'


    # 初始请求
    def start_requests(self):
        param = {
            'startDate': self.startDate,
            'endDate': self.endDate,
            'page': 1
        }
        yield scrapy.Request(url=self.url,
                                headers=self.headers,
                                body=self.payload.format(**param),
                                method='POST',
                                callback=self.parse,
                                meta = {'param':param}
                                )

    # 爬取列表页
    def parse(self, response):
        pages = response.xpath('//*[@id="mainModuleContainer_485_1113_1539_tdExtendProContainer"]/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]/text()').extract_first()
        if not pages:
            pages = 1
        else:
            start, end = re.search(r'共\d+页', pages).span()
            pages = int(pages[start+1:end-1])
        
        # 对列表中的每一项爬取详情
        for each in response.xpath('//*[@id="TAB_contentTable"]//tr[@class="gridItem" or @class="gridAlternatingItem"]'):
            url = each.xpath('td[3]/a/@href').extract_first()
            yield scrapy.Request(url=self.basic_url + url,
                                 headers=self.headers,
                                 method='POST',
                                 callback=self.parse_detail,
                                 )

        param = response.meta['param']
        if param['page'] < pages:
            param['page'] += 1
            yield scrapy.Request(url=self.url,
                        headers=self.headers,
                        body=self.payload.format(**param),
                        method='POST',
                        callback=self.parse,
                        meta = {'param':param}
                        )

    # 爬取详情页
    def parse_detail(self, response):

        item = LandcrawlerItem()
        item['area'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract_first()
        item['date'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()').extract_first()
        item['price'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract_first()
        item['purpose'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()').extract_first()
        item['supply'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()').extract_first()
        item['location'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()').extract_first()
        item['district'] = response.xpath(
            '//*[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract_first()

        # 交由pipline处理
        yield item
