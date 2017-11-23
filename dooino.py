#!/usr/bin/env python

import logging
import redis
import datetime

import custom_logging

logger = logging.getLogger(__name__)

class Dooino:
    REDIS_KEY = "dooinos"

    def __init__(self, name):
        logger.info("Loading dooino")
        self.name = name
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)

    def set(self, name, value):
        self.redis.hset(self.name, name, value)

    def get(self, name):
        return self.redis.hget(self.name, name)

    def touch(self):
        self.set("updated_at", datetime.datetime.now())

    def register(self):
        self.redis.sadd(self.REDIS_KEY, self.name)

    def destroy(self):
        self.redis.srem(self.REDIS_KEY, self.name)
        self.redis.delete(self.name)
