#!/usr/bin/python3
"""
3. Status of your API
The first endpoint that returns the status of your API
"""
from flask import Flask as fl
from flask import jsonify as jsny
from models import storage
from api.v1.views import app_views

# App name and start
app = fl(__name__)
# Blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def sessEnd(error):
    """Closes session to free up resources"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
