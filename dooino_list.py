#!/usr/bin/env python

import logging
import redis

import custom_logging

logger = logging.getLogger(__name__)

class DooinoList:
    REDIS_KEY = "dooinos"

    def __init__(self):
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)

    def run(self):
        return self.redis.smembers("dooinos")
