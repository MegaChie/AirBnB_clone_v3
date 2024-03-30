#!/usr/bin/python3
"""
6. State
  - Contains the API setup for the State object.
"""
from api.v1.views import app_views
from flask import abort
import json
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def stateEdit(state_id=None):
    """
    Edit the State objects according to the specified HTTP method:
      - GET: Retrieves the list of all State objects.
    """
    # Importing needed files
    from models.state import State
    # All states objects
    fullList = storage.all(State)

    if not state_id:
        # Getting a State at a time
        data = []
        for name in fullList.values():
            entry = name.to_dict()
            data.append(entry)
        return (json.dumps(data, indent=2),
                {"Content-Type": "application/json"})
    # When there's an ID
    seek = "State." + state_id
    # Search for the value
    try:
        found = fullList[seek].to_dict()
        return (json.dumps(found, indent=2),
                {"Content-Type": "application/json"})
    except KeyError:
        abort(404)
