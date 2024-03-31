#!/usr/bin/python3
"""Amenity View"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def getAmenities():
    """list amenties"""
    list_amenti = storage.all(Amenity)
    return jsonify([a.to_dict() for a in list_amenti.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    """get specefic amentiy"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """deletes an amenity"""
    a = storage.get("Amenity", amenity_id)
    if not a:
        abort(404)
    a.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def newAmenity():
    """new amenity"""
    amenty = request.get_json()
    if not amenty:
        abort(400, "Not a JSON")

    if "name" not in amenty:
        abort(400, "Missing name")

    amenity = Amenity(**amenty)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update(amenity_id):
    """update amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    request = request.get_json()
    if not request:
        abort(400, "Not a JSON")
    for key, value in request.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
