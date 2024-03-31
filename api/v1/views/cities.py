#!/usr/bin/python3
"""Define the API endpoint for City objects"""
from api.v1.views import app_views
from flask import jsonify as jsny, abort, request as req
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def cityAPI(state_id):
    """
    GET: Retrieves the list of all City objects if no ID is passed.
         Or all the cities in a sertain state if an ID is passed.
    """
    # All states and Cities
    fullState = storage.all(State)
    fullCity = storage.all(City)

    # Using HTTP GET
    if req.method == "GET":
        #seek = "State." + state_id
        #try:
         #   data = []
          #  found = fullState[seek]
            # data = [city.to_dict() for city in found.fullCity]
           # for city in found.fullCity:
            #    entry = city.to_dict()
             #   data.append(entry)
            #retrun (json.dumps(data, indent=2),
             #       {"Content-Type": "application/json"})
        #except KeyError:
          #  abort(404)
