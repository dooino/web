#!/usr/bin/env python

import logging
import custom_logging

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from dooino import Dooino
from dooino_list import DooinoList

from routine import Routine
from routine_list import RoutineList

app = Flask(__name__)

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
        params = request.get_json()
        data = {}

        for key in params:
            data[key] = params.get(key)

        Routine(data).save()

        return jsonify({})
    else:
        return jsonify(RoutineList().run())

@app.route("/dooinos")
def dooinos():
    data = []

    for entry in DooinoList().run():
        device = Dooino(entry)
        data.append(device.serialize())

    return jsonify(data)

@app.route("/templates/<template>.html")
def template(template):
    return render_template(template + ".html"), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
