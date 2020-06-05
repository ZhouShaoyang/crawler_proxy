# -*- coding: utf-8 -*-

import os
import sys
ROOT = os.getcwd()
sys.path.append(ROOT)

import traceback
import uvicorn
from fastapi import FastAPI

import config.setting as setting
import db.redisdb as redis


redis = redis.RedisConnect()
api = FastAPI()


@api.get('/getALL')
def get_all():
    try:
        result = redis.hash_get_checked()
        return {
            'success': 1,
            'data': result
        }
    except Exception:
        return {
            'success': 0,
            'data': traceback.format_exc()
        }


@api.get('/getCOUNT')
def get_count():
    try:
        result = redis.hash_count_checked()
        return {
            'success': 1,
            'data': result
        }
    except Exception:
        return {
            'success': 0,
            'data': traceback.format_exc()
        }

if __name__ == "__main__":
    uvicorn.run('api:api', host='0.0.0.0', port=20001, reload=True, workers=4)