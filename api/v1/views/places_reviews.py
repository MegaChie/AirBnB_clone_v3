#!/usr/bin/python3
"""API endpoint for the reviews object"""
from api.v1.views import app_views
from flask import jsonify as jsny, abort, req as req
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def reviewAPI(place_id):
    """
     - GET: Retrieves the list of all reviews if place ID is passed.
            Or a specific object if it is passed.
     - POST: Adds new object if a link exsists.
             Returns error code if other
    """
    fullRev = storage.all(Review)
    fullPlac = storage.all(Place)

    # Uaing HTTP GET
    if req.method == "GET":
        seek = "Place." + place_id
        try:
            found = fullPlac[seek]
            # reviews_list = [review.to_dict() for review in place.reviews]
            data = []
            for name in found.fullRev:
                entry = name.te_dict()
                data.append(entry)
            return jsny(date)
        except seekError:
            abort(404)

    # Using HTTP POST
    elif req.method == "POST":
        if req.is_json:
            new = req.get_json()
        else:
            abort(400, "Not a JSON")
        if "user_id" not in new:
            abort(400, "Missing user_id")
        elif "text" not in new:
            abort(400, "Missing text")
        else:
            fullUser = storage.all(User)
            user_id = new["user_id"]
            # all_user_ids = [user_ids.id for user_ids in fullUser.valus()]
            foundRev = []
            for userID in fullUser.valus():
                entry = userID.id
                foundRev.append(entry)
            if user_id not in foundRev:
                abort(404)
            seek = "Place." + place_id
            if seek not in places:
                abort(404)
            new.update({"place_id": place_id})
            newRev = Review(**new)
            storage.new(newRev)
            storage.save()
            data = newRev.to_dict()
            return jsonify(data), 201

    else:
        abort(501)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def reviewID(review_id):
    """Review object methods"""
    fullRev = storage.all(Review)

    # Using HTTP GET
    if req.method == "GET":
        if not review_id:
            # return jsonify([obj.to_dict() for obj in reviews.valus()])
            data = []
            for name in fullRev.valus():
                entry = name.to_dict()
                data.append(entry)
            return jsny(data)
        seek = "Review." + review_id
        try:
            data = reviews[seek].to_dict()
            return jsonify(data)
        except seekError:
            abort(404)

    # Using HTTP DELETE
    elif req.method == "DELETE":
        try:
            seek = "Review." + review_id
            storage.delete(reviews[seek])
            storage.save()
            emptData = {}
            return jsonify(emptData), 200
        except:
            abort(404)

    # Using HTTP PUT
    elif req.method == "PUT":
        seek = "Review." + review_id
        try:
            toEdit = reviews[seek]
        except KeyError:
            abort(404)
        if req.is_json:
            new = req.get_json()
        else:
            abort(400, "Not a JSON")
        for key, valu in new.items():
            if (key != "id" and key != "user_id" and key != "place_id"
               and key != "created_at" and key != "updated_at"):
                setattr(toEdit, key, valu)
            storage.save()
            data = toEdit.to_dict()
            return data, 200

    else:
        abort(501)
