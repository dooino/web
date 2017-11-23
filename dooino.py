#!/usr/bin/env python

import logging
import redis
import datetime

import custom_logging
from features_fetcher import FeaturesFetcher

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

    def manifest_url(self):
        return "http://" + self.get("ip") + "/manifest.json"

    def touch(self):
        self.set("updated_at", datetime.datetime.now())
        self.set("online", 1)

    def register(self):
        self.redis.sadd(self.REDIS_KEY, self.name)

    def fetch(self):
        features = FeaturesFetcher(self)
        features.fetch()

        for key in features.data:
            self.set(key, features.data[key])

        return features.data

    def serialize(self):
        data = {}
        remote_data = self.fetch()
        local_data = self._serialize()

        data.update(local_data)
        data.update(remote_data)

        for key in data:
            if data[key] == "1":
                data[key] = True
            elif data[key] == "0":
                data[key] = False

        return data

    def _serialize(self):
        data = {}

        for key in self.redis.hkeys(self.name):
            data[key] = self.get(key)

        return data

    def online(self):
        return self.get("online")

    def take_offline(self):
        self.set("online", 0)

    def destroy(self):
        self.redis.srem(self.REDIS_KEY, self.name)
        self.redis.delete(self.name)
