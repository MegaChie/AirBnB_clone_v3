#!/usr/bin/python3
"""Amenity View"""
from api.v1.views import app_views
from flask import jsonify as jsny, abort, request as req
from models import storage


@app_views.route("/amenities", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenAPI(amenity_id=None):
    """
     - GET: Retrieves the list of all Amenity objects if no ID passed.
            One object with ID passed.
     - DELETE: Remove object if ID passed.
               Return error code if ID is none or incorrect.
     - POST: Add object if name is passed.
             Returns error code if not passed or input is bad.
     - PUT: Updates object if input is correct. Returns error code otherwise.
    """
    from models.amenity import Amenity
    fullList = storage.all(Amenity)

    # Using HTTP GET
    if req.method == "Get":
        # All is returned
        if not amenity_id:
            data = []
            for name in fullList.values():
                entry = name.to_dict()
                data.append(entry)
            return jsny(data)
        # ID passed
        seek = "Amenity." + amenity_id
        try:
            found = fullList[seek]
            data = found.to_dict()
            return jsny(data), 200
        except KeyError:
            abort(404)

    # Using HTTP DELETE
    if req.method == "DELETE":
        try:
            seek = "Amenity." + amenity_id
            storage.delete(fullList[seek])
            storage.save()
            emptData = {}
            return jsny(emptData), 200
        except Exception:
            abort(404)

    # Using HTTP POST
    if req.method == "POST":
        if req.is_json:
            new = req.get_json()
        else:
            abort(400, "Not a JSON")
        if "name" in new:
            newAmen = Amenity(**new)
            storage.new(newAmen)
            storage.save()
            data = newAmen.to_dict()
            return jsny(data), 201
        else:
            abort(400, "Missing name")

    # Using HTTP PUT
    if req.method == "PUT":
        seek = "Amenity." + amenity_id
        try:
            toEdit = fullList[seek]
            if req.is_json:
                edit = req.get_json()
            else:
                abort(400, "Not a JSON")
            for key, valu in edit.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(toEdit, key, valu)
            storage.save()
            data = toEdit.to_dict()
            return jsny(data), 200
        except KeyError:
            abort(404)

    else:
        abort(501)
