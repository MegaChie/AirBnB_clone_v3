#!/usr/bin/python3
"""Gives the API its status"""
from api.v1.views import app_views
from flask import jsonify as jsny
from models import storage
import json


@app_views.route('/status', strict_slashes=False)
def getStat():
    """returns the status of the API if working"""
    goodStat = {'status': 'OK'}
    return jsny(goodStat), 200
#    return (json.dumps(goodStat, indent=2),
 #           {"Content-Type": "application/json"}, 200)


@app_views.route('/stats', strict_slashes=False)
def counter():
    """Build a dict of classes count using the count method"""
    # importing classes
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    # look up dict
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    # empty dict to fill using the method
    clasCount = {}
    for name, cls in classes.items():
        clasCount.update({name: storage.count(cls)})
    return jsny(clasCount), 200
 #   return (json.dumps(clasCount, indent=2),
#            {"Content-Type": "application/json"})


@app_views.after_request
def add_newline(response):
    if response.is_json:
        response.data += b'\n'
    return response
