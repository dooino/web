#!/usr/bin/env python

import logging
import redis
import json
import requests
import time

import custom_logging

logger = logging.getLogger(__name__)

class Requester:
    def __init__(self, url):
        self.url = url

    def run(self):
        try:
            data = requests.get(self.url).json()
            return data["value"]
        except Exception:
            logger.fatal("Could not connect", exc_info=True)
            return None


class Executor:
    def __init__(self, url):
        self.url = url

    def run(self):
        try:
            requests.get(self.url)
        except Exception:
            logger.fatal("Could not execute", exc_info=True)
            return None


class Checker:
    def __init__(self, output, input, operation):
        self.output = int(output)
        self.input = int(input)
        self.operation = int(operation)

    def run(self):
        logger.debug("Checking %s agains %s", self.output, self.input)

        if self.operation is 0:
            logger.debug("equal")
            return self.output == self.input
        elif self.operation is 1:
            logger.debug("greater")
            return self.output > self.input
        elif self.operation is 2:
            logger.debug("smaller")
            return self.output < self.input
        else:
            logger.debug("operation failed")
            return False


class Processor:
    def __init__(self, routine):
        self.routine = routine

    def run(self):
        out = Requester(self.routine["selectedOut"]).run()
        operation = self.routine["selectedOperation"]
        value = self.routine["selectedValue"]

        if Checker(out, value, operation).run():
            logger.info("Executing routine...")
            Executor(self.routine["selectedIn"]).run()
        else:
            logger.info("Skipping routine...")


class Worker:
    ROUTINES_KEY = "routines"

    def __init__(self):
        logger.info("Initializing worker...")
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def run(self):
        logger.info("Running...")
        routines = self.redis.smembers(self.ROUTINES_KEY)

        for data in routines:
            routine = json.loads(data)

            if self._is_valid_routine(routine):
                Processor(routine).run()

    def _is_valid_routine(self, routine):
        if(
            routine["selectedIn"] is None or
            routine["selectedOut"] is None or
            routine["selectedValue"] is None or
            routine["selectedOperation"] is None
           ):
            logger.fatal("Could not process routine: %s", routine)
            return False

        return True


if __name__ == "__main__":
    LOOP_TIME = 2
    while True:
        Worker().run()
        time.sleep(LOOP_TIME)
