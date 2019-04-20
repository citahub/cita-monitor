#!/usr/bin/python3
# -*- coding: utf-8 -*-

# demo for using package "requests-cache" to cache the API request result, store cached data in a sqlite db as "cita_testnet_jsonrpc_cache.sqlite"

import requests
import requests_cache # doc: https://requests-cache.readthedocs.io/en/latest/
import time

# doc: http://flask.pocoo.org/docs/1.0/
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
requests_cache.install_cache('cita_testnet_jsonrpc_cache', backend='sqlite', expire_after=180, allowable_methods="POST")
cita_testnet_rpc_url = "https://node.cryptape.com"

# e.g.: http://localhost:5000/blockNumber
# curl -s -d '{"id": 1, "jsonrpc": "2.0", "method":"blockNumber","params": []}' -H 'content-type:application/json' https://node.cryptape.com
@app.route('/blockNumber', methods=['GET'])
def blockNumber():
    with requests_cache.disabled():
        payload = '{"id": 1, "jsonrpc": "2.0", "method":"blockNumber","params": []}'
        now = time.ctime(int(time.time()))
        response = requests.post(cita_testnet_rpc_url, payload)
        print("Time: {0} / Used Cache: {1}".format(now, hasattr(response, "from_cache")))
        return jsonify(response.json())

# e.g.: http://localhost:5000/getBlockByNumber/0x499d71
# curl -s -d '{"id": 1, "jsonrpc": "2.0", "method":"getBlockByNumber","params": ["0x499d71", false]}' -H 'content-type:application/json' https://node.cryptape.com
@app.route('/getBlockByNumber/<quantity>', methods=['GET'])
def getBlockByNumber(quantity):
    payload = '{"id": 1, "jsonrpc": "2.0", "method":"getBlockByNumber","params": ["'+quantity+'", false]}'
    now = time.ctime(int(time.time()))
    response = requests.post(cita_testnet_rpc_url, payload)
    print("Time: {0} / Used Cache: {1}".format(now, response.from_cache))
    return jsonify(response.json())

# run "python cita-jsonrpc-api-cache-demo.py"
if __name__ == '__main__':
    app.run(debug=True)
