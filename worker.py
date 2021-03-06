#!/usr/bin/env python

import logging
import redis
import json
import requests
import time
import os

import custom_logging

from routine_list import RoutineList
from dooino import Dooino

logger = logging.getLogger(__name__)

class Ping:
    def __init__(self, host):
        self.host = host
        logger.fatal(host)

    def run(self):
        ip = self._parse_ip(self.host)
        response = os.system("ping -c 1 -W 200 " + ip)

        if response is 0:
            return True

        return False

    def _parse_ip(self, ip):
        return ip.split(":")[0]


class Requester:
    def __init__(self, source):
        self.source = source
        self.dooino = Dooino(source["id"])

    def run(self):
        try:
            url = self.dooino.get_out_action(self.source["action"])
            data = requests.get(url, timeout=1).json()
            return data["value"]
        except Exception:
            logger.fatal("Could not connect", exc_info=True)
            return None


class Executor:
    def __init__(self, target):
        self.target = target
        self.dooino = Dooino(target["id"])

    def run(self):
        try:
            url = self.dooino.get_in_action(self.target["action"])
            requests.get(url, timeout=0.5)
        except Exception:
            logger.fatal("Could not execute", exc_info=True)
            return None


class Checker:
    def __init__(self, output, input, operation):
        self.output = output
        self.input = input
        self.operation = operation

    def run(self):
        logger.debug("Checking %s agains %s", self.output, self.input)

        if self.output == "null" or self.output is None or self.input is None or self.operation is None:
            return False

        output = float(self.output)
        input = float(self.input)
        operation = int(self.operation)

        if operation is 0:
            logger.debug("equal")
            return output == input
        elif operation is 1:
            logger.debug("greater")
            return output > input
        elif operation is 2:
            logger.debug("smaller")
            return output < input
        else:
            logger.debug("operation failed")
            return False


class Processor:
    def __init__(self, routine):
        self.routine = routine

    def run(self):
        out = Requester(self.routine["source"]).run()
        operation = self.routine["condition"]["operation"]
        value = self.routine["condition"]["value"]

        if Checker(out, value, operation).run():
            logger.info("Executing routine...")
            Executor(self.routine["target"]).run()
        else:
            logger.info("Skipping routine...")


class PresenceWorker:
    DOOINOS_KEY = "dooinos"

    def __init__(self):
        logger.info("Checking presence of devices...")
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def run(self):
        logger.info("Running check...")
        devices = self.redis.smembers(self.DOOINOS_KEY)
        keys_to_delete = []

        for device in devices:
            ip = self.redis.get(device)
            url = "http://" + ip + "/manifest.json"

            if Ping(ip).run():
                logger.info("Device is present: %s(%s)", device, ip)
            else:
                keys_to_delete.append(device)
                logger.fatal("Device is not present", exc_info=True)

        for key in keys_to_delete:
            self.redis.srem(self.DOOINOS_KEY, key)


class RoutineWorker:
    def __init__(self):
        logger.info("Initializing worker...")

    def run(self):
        logger.info("Running...")

        for data in RoutineList().run():
            routine = data

            if self._is_valid_routine(routine):
                Processor(routine).run()

    def _is_valid_routine(self, routine):
        if(
            routine.get("source", {}).get("id") is None or
            routine.get("source", {}).get("action") is None or
            routine.get("target", {}).get("id") is None or
            routine.get("target", {}).get("action") is None or
            routine.get("condition", {}).get("value") is None or
            routine.get("condition", {}).get("operation") is None
           ):
            logger.fatal("Could not process routine: %s", routine)
            return False

        return True


if __name__ == "__main__":
    LOOP_TIME = 5
    while True:
        # PresenceWorker().run()
        RoutineWorker().run()

        time.sleep(LOOP_TIME)
