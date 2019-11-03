# -*- coding: utf-8 -*-
# @Date    : 2019-11-03
# @Author  : 惜命命
# @model   : 代理池.动态调用crawl开头的方法获取代理存入redis

import sys
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
