#!/usr/bin/env python

import logging

import custom_logging
from features_fetcher import FeaturesFetcher
from redis_interface import RedisInterface

from dooino import Dooino

logger = logging.getLogger(__name__)

class Setup(RedisInterface):
    REDIS_KEY = "dooinos"

    def __init__(self, name, ip):
        logger.info("Setting up dooino")
        self.name = name
        self.ip = ip

    def register(self):
        dooino = Dooino(self.name)
        dooino.set("ip", self.ip)

        features = FeaturesFetcher(dooino)
        features.fetch()

        dooino.destroy()

        dooino = Dooino(features.data["id"])
        dooino.register()
        dooino.set("ip", self.ip)
        dooino.fetch()

    def destroy(self):
        self.redis.srem(self.REDIS_KEY, self.name)
        self.redis.delete(self.name)
