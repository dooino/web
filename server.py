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
from dooino import Dooino

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
logger = logging.getLogger(__name__)

@app.route("/")
def dashboard():
    return render_template('application.html')

@app.route("/new")
def new():
    return render_template('application.html')

@app.route("/routines", methods=['POST', 'GET'])
def routines():
    if request.method == 'POST':
        info = request.get_json()
        data = {
            'selectedIn': info.get('selectedIn'),
            'selectedOut': info.get('selectedOut'),
            'selectedValue': info.get('selectedValue'),
            'selectedOperation': info.get('selectedOperation'),
            'selectedInDooino': info.get('selectedInDooino'),
            'selectedOutDooino': info.get('selectedOutDooino'),
        }

        r.sadd('routines', json.dumps(data))

        return jsonify({})
    else:
        data = []

        for routine in r.smembers('routines'):
            data.append(json.loads(routine))

        return jsonify(data)

@app.route("/dooinos")
def dooinos():
    data = []

    for entry in r.smembers("dooinos"):
        device = Dooino(entry)
        device.touch()
        feature = FeaturesFetcher(device.get("ip"))
        feature.fetch()
        new_data = feature.data
        new_data["updated_at"] = device.get("updated_at")
        data.append(new_data)

    return jsonify(data)

@app.route("/templates/<template>.html")
def template(template):
    return render_template(template + ".html"), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
