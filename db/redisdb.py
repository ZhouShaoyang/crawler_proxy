# -*- coding: utf-8 -*-

import os
import sys
ROOT = os.getcwd()
sys.path.append(ROOT)

import redis
import json
from random import sample

import config.setting as setting


class RedisConnect():

    def __init__(self):
        self.host = setting.REDIS_HOST
        self.port = setting.REDIS_PORT
        self.name_original = setting.REDIS_NAME_ORIGINAL
        self.name_checked = setting.REDIS_NAME_CHECKED
        self.redisdb = redis.StrictRedis(host=self.host, port=int(self.port), db=0, decode_responses=True)

    def hash_set_original(self, key, value):
        self.redisdb.hset(name=self.name_original, key=json.dumps(key), value=str(value))

    def hash_set_checked(self, key, value):
        self.redisdb.hset(name=self.name_checked, key=json.dumps(key), value=str(value))

    def hash_del_original(self, key):
        self.redisdb.hdel(self.name_original, json.dumps(key))

    def hash_del_checked(self, key):
        self.redisdb.hdel(self.name_checked, json.dumps(key))

    def hash_count_original(self):
        return self.redisdb.hlen(name=self.name_original)
    
    def hash_count_checked(self):
        return self.redisdb.hlen(name=self.name_checked)

    def hash_getall_original(self, count=None):
        ips = []
        for key, value in self.redisdb.hgetall(name=self.name_original).items():
            ips.append(json.loads(key))
        if type(count) == int and self.redisdb.hlen(name=self.name_original) > count:
            return sample(ips, count)
        else:
            return ips
    
    def hash_getall_checked(self, count=None):
        ips = []
        for key, value in self.redisdb.hgetall(name=self.name_checked).items():
            ips.append(json.loads(key))
        if type(count) == int and self.redisdb.hlen(name=self.name_checked) > count:
            return sample(ips, count)
        else:
            return ips

    def hash_gethttp_checked(self, count=None):
        ips = []
        for key, value in self.redisdb.hgetall(name=self.name_checked).items():
            if value == 'http':
                ips.append(json.loads(key))
        if type(count) == int and self.redisdb.hlen(name=self.name_checked) > count:
            return sample(ips, count)
        else:
            return ips

    def hash_gethttps_checked(self, count=None):
        ips = []
        for key, value in self.redisdb.hgetall(name=self.name_checked).items():
            if value == 'https':
                ips.append(json.loads(key))
        if type(count) == int and self.redisdb.hlen(name=self.name_checked) > count:
            return sample(ips, count)
        else:
            return ips
