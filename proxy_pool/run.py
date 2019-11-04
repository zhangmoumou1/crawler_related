# -*- coding: utf-8 -*-
# @Date    : 2019-11-03
# @Author  : 惜命命
# @model   : 主执行文件

from proxypool.scheduler import Scheduler
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
