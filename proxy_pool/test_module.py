
# -*- coding: utf-8 -*-
# @Date    : 2019-11-03
# @Author  : 惜命命
# @model   : 代理池.检测模块

import sys
sys.path.append('./proxy_pool')
import time, aiohttp, asyncio
from memory_module import RedisClient

valid_status_codes = [200]
test_url = 'http://www.baidu.com'
batch_test_size = 100

class Tester(object):
    """
    检测模块
    """
    def __init(self):
        self.redis = RedisClient

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 单个代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(test_url, proxy=real_proxy, timeout=15) as response:
                    if response.status in valid_status_codes:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (ConnectionError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            #批量测试
            for i in range(0, len(proxies), batch_test_size):
                test_proxies = proxies[i:i + batch_test_size]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
