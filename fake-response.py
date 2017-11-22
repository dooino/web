#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({'value': 10})

@app.route("/on")
def on():
    return jsonify({})

@app.route("/off")
def off():
    return jsonify({})

@app.route("/manifest.json")
def fake():
    return jsonify(
            {
                'name': 'dooino-xyz',
                'in': [
                    {
                        'name': 'on',
                        'action': 'http://127.0.0.1:6000/on'
                    },
                    {
                        'name': 'off',
                        'action': 'http://127.0.0.1:6000/off'
                    }
                ],
                'out': [
                    {
                        'name': 'status',
                        'action': 'http://127.0.0.1:6000/status'
                    }
                ],
                'version': 123,
                'capabilities': [],
            })

if __name__ == "__main__":
    app.run(host= '0.0.0.0',port=6000)
