#!/usr/bin/python3
"""API endpoint for the reviews object"""
from api.v1.views import app_views
from flask import jsonify as jsny, make_response, abort, req as req
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
            return jsny(data)
        except:
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
            return jsny(data), 201

    else:
        abort(501)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReview(review_id):
    """get Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsny(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def DeleteReview(review_id):
    """delete Review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsny({}), 200)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def putReview(review_id):
    """put review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    reques = req.get_json()
    if not reques:
        abort(400, "Not a JSON")
    for k, value in reques.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, value)
    storage.save()
    return make_response(jsny(review.to_dict()), 200)

