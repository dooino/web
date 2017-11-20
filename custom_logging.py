import logging

LOG_FILENAME = "log.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format="%(asctime)s %(levelname)s - (%(funcName)s) - %(message)s")
