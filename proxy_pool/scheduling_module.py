# -*- coding: utf-8 -*-
# @Date    : 2019-11-03
# @Author  : 惜命命
# @model   : 代理池.调度模块--将其他模块运行起来

import sys
sys.path.append('./proxy_pool')

tester_cycle = 20
getter_cycle = 20
tester_enabled = True
getter_enabled = True
api_enabled = True

import time
from multiprocessing import Process
from interface_module import app
from obtain_module import Getter
from test_module import Tester

class Scheduler(object):
    def schedule_tester(self, cycle=tester_cycle):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=getter_cycle):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api
        """
        app.run(api_host='127.0.0.1', api_port='5555')

    def run(self):
        print('代理池开始运行')
        if tester_enabled:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if getter_enabled:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if api_enabled:
            api_process = Process(target=self.schedule_api)
            api_process.start()

Scheduler().run()