#!/usr/bin/env python

import logging
import json
import redis

import custom_logging

logger = logging.getLogger(__name__)

class Routine:
    REDIS_KEY = "routines"

    def __init__(self, data):
        self.data = data
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)

    def save(self):
        self.redis.sadd(self.REDIS_KEY, json.dumps(self.data))
