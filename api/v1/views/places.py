#!/usr/bin/python3
'''place View'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import requests
import json
from os import getenv


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def listPlaces(city_id):
    """get Places list"""
    cuty = storage.get(City, city_id)
    if not cuty:
        abort(404)

    return jsonify([pla.to_dict() for pla in cuty.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlace(place_id):
    """get Specefic place"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """delete place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def newPlace(city_id):
    """new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    pla = request.get_json()
    if not pla:
        abort(400, 'Not a JSON')
    if 'user_id' not in pla:
        abort(400, "Missing user_id")
    uid = pla['user_id']
    usr = storage.get(User, uid)
    if not usr:
        abort(404)
    if 'name' not in pla:
        abort(400, "Missing name")
    place = Place(**pla)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def updatePlace(place_id):
    """updatePlace"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reques = request.get_json()
    if not reques:
        abort(400, "Not a JSON")

    for key, value in reques.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
