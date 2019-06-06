#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class UrlManager:
    def __init__(self):
    	#管理的是元组（district，url）的列表
	    self.urls = list()

    def add_url(self,url):
    	if url is None or url == "":
    	   return
        #if url not in self.urls:
        self.urls.append(url)

    def add_urls(self, urls):
    	if urls is None or len(urls) == 0:
    	   return
    	for url in urls:
    		self.add_url(url)

    def has_url(self):
    	return len(self.urls) != 0 

    def get_url(self):
    	return self.urls.pop()

    def get_length(self):
    	return len(self.urls)