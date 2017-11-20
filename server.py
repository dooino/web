#!/usr/bin/env python

import logging
import redis
import custom_logging

from flask import Flask
from flask import render_template
from flask import jsonify

from features_fetcher import FeaturesFetcher

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
logger = logging.getLogger(__name__)

@app.route("/")
def dashboard():
    data = []

    for entry in r.smembers('dooinos'):
        feature = FeaturesFetcher(r.get(entry))
        feature.fetch()
        data.append(feature.data)

    return render_template('list.html', entries=data)

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
