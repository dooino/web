#!/usr/bin/env python

import logging
import redis
import json
import custom_logging

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from features_fetcher import FeaturesFetcher

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
logger = logging.getLogger(__name__)

@app.route("/")
def dashboard():
    return render_template('application.html')

@app.route("/new")
def new():
    return render_template('application.html')

@app.route("/routines", methods=['POST'])
def routines():
    info = request.get_json()
    data = {
            'selectedIn': info.get('selectedIn'),
            'selectedOut': info.get('selectedOut'),
            'selectedValue': info.get('selectedValue'),
            'selectedOperation': info.get('selectedOperation'),
    }

    r.sadd('routines', json.dumps(data))

    return jsonify({})

@app.route("/dooinos")
def dooinos():
    data = []

    for entry in r.smembers('dooinos'):
        feature = FeaturesFetcher(r.get(entry))
        feature.fetch()
        data.append(feature.data)

    return jsonify(data)

@app.route("/templates/<template>.html")
def template(template):
    return render_template(template + ".html"), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
