# -*- coding: utf-8 -*-

import os
import sys
ROOT = os.getcwd()
sys.path.append(ROOT)

import time
import json
import grequests
from bs4 import BeautifulSoup

import config.setting as setting
import db.redisdb as redis


class Check():
    
    def __init__(self):
        self.redis = redis.RedisConnect()
        self.url = setting.CHECKING_URL
        self.headers = setting.CHECKING_HEADERS
        self.sample = setting.SAMPLE
        self.timeout = setting.TIMEOUT

    def count_original(self):
        return self.redis.hash_count_original()
    
    def count_checked(self):
        return self.redis.hash_count_checked()

    def check_original(self):
        try:
            proxys = [proxy for proxy in self.redis.hash_get_original(count=self.sample)]
            requests = [grequests.get(url=self.url, headers=self.headers, proxies=proxy, timeout=self.timeout) for proxy in proxys]
            responses = grequests.map(requests)
            for item in zip(proxys, responses):
                proxy, response = item[0], item[1]
                try:
                    if response.status_code == 200:
                        self.redis.hash_set_checked(proxy, response.elapsed.total_seconds())
                except Exception:
                    pass
                self.redis.hash_del_original(proxy)
                setting.logging.info(f'[REMOVE] [ORIGINAL] [{proxy}]')    
        except Exception as error:
            setting.logging.error(f'[ERROR] [CHECK] [ORIGINAL] - CAUSE: {error}')
    
    def check_checked(self):
        try:
            proxys = [proxy for proxy in self.redis.hash_get_checked(count=self.sample)]
            requests = [grequests.get(url=self.url, headers=self.headers, proxies=proxy, timeout=self.timeout) for proxy in proxys]
            responses = grequests.map(requests)
            for item in zip(proxys, responses):
                proxy, response = item[0], item[1]
                try:
                    response.status_code == 200
                except Exception:
                    self.redis.hash_del_checked(proxy)
                    setting.logging.info(f'[REMOVE] [CHECKED] [{proxy}]')
        except Exception as error:
            setting.logging.error(f'[ERROR] [CHECK] [CHECKED] - CAUSE: {error}')


c = Check()
while True:
    if c.count_original() < 1 and c.check_checked < 1:
        time.sleep(setting.TIME_CHECK)
    elif c.count_original() >= 1 and c.count_checked() < setting.PROXY_MIN:
        c.check_original()
        time.sleep(setting.TIME_CHECK)
    else:
        c.check_checked()
        c.check_original()
        time.sleep(setting.TIME_CHECK * 10)
