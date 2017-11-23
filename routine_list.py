#!/usr/bin/env python

import logging
import redis
import json

import custom_logging

from routine import Routine

logger = logging.getLogger(__name__)

class RoutineList:
    REDIS_KEY = "routines"

    def __init__(self):
        self.redis = redis.StrictRedis(host="localhost", port=6379, db=0)

    def run(self):
        data = []

        for routine in self.redis.smembers(self.REDIS_KEY):
            data.append(json.loads(routine))

        return data
