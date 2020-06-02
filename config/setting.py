# -*- coding: utf-8 -*-

import os
import sys
ROOT = os.getcwd()
sys.path.append(ROOT)

import logging


# REDIS SETTING
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '19922'
REDIS_NAME_ORIGINAL = 'crawler_proxy_original'
REDIS_NAME_CHECKED = 'crawler_proxy_checked'

# CRAWL SETTING
PROXY_HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
SLEEP = 3

# CHECK SETTING
CHECKING_URL = 'https://www.baidu.com'
CHECKING_HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
SAMPLE = 500
TIMEOUT = 10

# SCHEDULE SETTING
PROXY_MIN = 1000
TIME_CHECK = 30
TIME_CRAWL = 28800

# LOGGING SETTING
LOG_FORMAT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
FILENAME = f'{ROOT}/log/crawler_proxy.log'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, filename=FILENAME)
