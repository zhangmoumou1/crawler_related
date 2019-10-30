max_score = 100
min_score = 0
initial_score = 10
redis_host = 'xxxxxxx'
redis_port = 6397
redis_password = 'xxxxxx'
redis_key = 'proxies'

import redis
from random import choice

class RedisClient(object):
    def __init__(self, host=redis_host, port=redis_port, password=redis_password):
        """
        初始化
        :return: 登录redis
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=initial_score):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(redis_key, proxy):
            return self.db.zadd(redis_key, score, proxy)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(redis_key, max_score, max_score)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(redis_key, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(redis_key, proxy)
        if score and score > min_score:
            print('代理', proxy, '当前分数', score, '减1' )
            return self.db.zincrby(redis_key, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(redis_key, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(redis_key, proxy) == None

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print(' 代理 ', proxy, ' 可用，设置为 ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)