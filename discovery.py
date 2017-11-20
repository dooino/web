#!/usr/bin/env python

""" Example of browsing for a service (in this case, HTTP) """

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import socket
import sys
from time import sleep
import redis
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

import custom_logging

REDIS_KEY = "dooinos"

logger = logging.getLogger("dooino")
r = redis.StrictRedis(host="localhost", port=6379, db=0)

def on_service_state_change(zeroconf, service_type, name, state_change):
    logger.info("Service %s of type %s state changed: %s" % (name, service_type, state_change))
    logger.info("State change: %s" % state_change)

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            logger.info("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            logger.info("  Weight: %d, priority: %d" % (info.weight, info.priority))
            logger.info("  Server: %s" % (info.server,))

            r.sadd(REDIS_KEY, name)
            r.set(name, "%s:%d" % (socket.inet_ntoa(info.address), info.port))

            if info.properties:
                logger.info("  Properties are:")
                for key, value in info.properties.items():
                    logger.info("    %s: %s" % (key, value))
            else:
                logger.info("  No properties")
        else:
            logger.info("  No info")
        logger.info('\n')
    elif state_change is ServiceStateChange.Removed:
        logger.info("Removing %s" % (name))

        r.srem(REDIS_KEY, name)
        r.delete(name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    logger.info("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_dooino._tcp.local.", handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
