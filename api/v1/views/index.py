#!/usr/bin/python3
"""Gives the API its status"""
from api.v1.views import app_views
import json
from flask import jsonify as jsny


@app_views.route('/status')
def getStat():
    """returns the status of the API if working"""
    goodStat = {"status": "OK"}
    return json.dumps(goodStat, indent=2), {"Content-Type": "application/json"}


@app_views.after_request
def add_newline(response):
    if response.is_json:
        response.data += b'\n'
    return response
