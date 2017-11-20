#!/usr/bin/env python

import requests
import logging

logger = logging.getLogger(__name__)

class FeaturesFetcher:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.data = {}

    def fetch(self):
        if self.ip_address is None:
            logger.error("URL is None")
            return

        url = "http://" + self.ip_address + "/manifest.json"
        logger.info("Requesting URL: %s", url)

        try:
            data = requests.get("http://" + self.ip_address + "/manifest.json").json()
            self.data = data
            logger.info("Fetched data: %s", data)
        except Exception:
            logger.fatal("Could not connect", exc_info=True)
