#!/usr/bin/python3
"""Gives the API its status"""
from api.v1.views import app_views
from flask import jsonify as jsny


@app_views.route('/status')
def getStat():
    """returns the status of the API if working"""
    goodStat = {"status": "OK"}
    return jsny(goodStat)
