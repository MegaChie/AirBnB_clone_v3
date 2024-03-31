#!/usr/bin/python3
"""
6. State
  - Contains the API setup for the State object.
"""
from api.v1.views import app_views
from flask import abort
from flask import request as req
import json
from models import storage


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET", "DELETE"],
                 strict_slashes=False)
def stateEdit(state_id=None):
    """
    Edit the State objects according to the specified HTTP method:
      - GET: Retrieves the list of all State objects.
             Or one object if ID is passed.
      - DELETE: Deletes object what have the passed ID.
                Or returns 404 page if no ID passed.
    """
    # Importing needed files
    from models.state import State
    # All states objects
    fullList = storage.all(State)

    # Using HTTP GET
    if req.method == "GET":
        if not state_id:
            # Getting a State at a time
            data = []
            for name in fullList.values():
                entry = name.to_dict()
                data.append(entry)
            return (json.dumps(data, indent=2, sort_keys=True),
                    {"Content-Type": "application/json"})
        # When there"s an ID
        seek = "State." + state_id
        # Search for the value
        try:
            found = fullList[seek].to_dict()
            return (json.dumps(found, indent=2, sort_keys=True),
                    {"Content-Type": "application/json"})
        except KeyError:
            abort(404)

    # Using HTTP DELETE
    elif req.method == "DELETE":
        # No ID passed
        if not state_id:
            abort(404)
        # ID passed
        try:
            seek = "State." + state_id
            # If found object with such ID
            storage.delete(fullList[seek])
            storage.save()
            emptData = {}
            return (json.dumbs(emptData),
                    {"Content-Type": "application/json"}, 200)
        except KeyError:
            # No object with such ID
            abort(404)

    # Using HTTP POST
    elif req.method == "POST":
        # Checking the heads passed
        if req.get_json:
            # If it's valid, save it
            new = req.get_json()
            # Use it
            if "name" in new:
                newState = State(**new)
                storage.new(newState)
                storage.save()
                data = newState.to_dict()
                return (json.dumps(data, indent=2),
                        {"Content-Type": "application/json"}), 201
            else:
                abort(400, "Missing name")
        else:
            # Abort!
            abort(400, "Not a JSON")
