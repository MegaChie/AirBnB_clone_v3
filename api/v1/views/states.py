#!/usr/bin/python3
"""
6. State
  - Contains the API setup for the State object.
"""
from api.v1.views import app_views
import json
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def stateEdit():
    """
    Edit the State objects according to the specified HTTP method:
      - GET: Retrieves the list of all State objects.
    """
    # Importing needed files
    from models.state import State
    # All states objects
    fullList = storage.all(State)
    # Getting a State at a time
    data = []
    for name in fullList.values():
        entry = name.to_dict()
        data.append(entry)
    return (json.dumps(data, indent=2), {"Content-Type": "application/json"})
