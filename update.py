import sys
import os
import pandas as pd
import gevent
from gevent import monkey
from CoronaVirus.utils import fetch_daily, URL, ONE_DAY, START_DAY, TODAY, download_data


if __name__ == '__main__':
    if len(sys.argv) == 1:
        hint = """
        参数1：[today, all]
        """
        print(hint)
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'today':
            fetch_daily()
        elif sys.argv[1] == 'all':
            monkey.patch_all()
            download_num = (TODAY - START_DAY).days
            urls = [(URL.format((START_DAY + i * ONE_DAY).strftime('%m-%d-%Y')),
                     (START_DAY + i * ONE_DAY).strftime('%m-%d-%Y') + '.csv') for i in range(download_num)]
            gevent.joinall([gevent.spawn(download_data, args[0], args[1]) for args in urls])
        else:
            print('命令有误，重新输入')
