#!/usr/bin/env python

import redis

class RedisInterface:
    def __init__(self):
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)
        self.name = "DEFAULT"

    def set(self, name, value):
        self.redis.hset(self.name, name, value)

    def get(self, name, value):
        self.redis.hset(self.name, name, value)
