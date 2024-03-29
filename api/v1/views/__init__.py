#!/usr/bin/python3
"""Support file for the API"""
from flask import Blueprint

# Blueprint import
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
