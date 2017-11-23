#!/usr/bin/env python

import requests
import logging

logger = logging.getLogger(__name__)

class FeaturesFetcher:
    def __init__(self, dooino):
        self.dooino = dooino
        self.data = {}

    def fetch(self):
        if self.dooino.get("ip") is None:
            logger.error("URL is None")
            return

        url = self.dooino.manifest_url()

        logger.info("Requesting URL: %s", url)

        try:
            data = requests.get(url, timeout=1).json()
            self.data = data
            self.dooino.touch()
            logger.info("Fetched data: %s", data)
        except Exception:
            self.dooino.take_offline()
            logger.fatal("Could not connect", exc_info=True)
