max_score = 100
min_score = 0
initial_score = 10
redis_host = 
redis_port = 
redis_password = 
redis_key = 

import redis
from random import choice

class RedisClient(object):
    def __init__(self, host=redis_host, port=redis_port, password=redis_password):
        """初始化"""
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)