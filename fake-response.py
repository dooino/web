#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/manifest.json")
def fake():
    return jsonify(
            {
                'name': 'dooino',
                'version': 123,
                'capabilities': [],
            })

if __name__ == "__main__":
    app.run(host= '0.0.0.0',port=6000)
