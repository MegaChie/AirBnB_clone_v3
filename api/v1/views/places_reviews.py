#!/usr/bin/python3
"""API endpoint for the reviews object"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
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
    reviews = storage.all(Review)
    places = storage.all(Place)

    # Using HTTP GET
    if req.method == "GET":
        place_key = "Place." + place_id
        try:
            place = places[place_key]
            reviews_list = [review.to_dict() for review in place.reviews]
            return jsonify(reviews_list)
        except KeyError:
            abort(404)

    # Using HTTP POST
    elif req.method == "POST":
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, "Not a JSON")
        if 'user_id' not in body_request:
            abort(400, "Missing user_id")
        elif 'text' not in body_request:
            abort(400, "Missing text")
        else:
            users = storage.all(User)
            user_id = body_request['user_id']
            all_user_ids = [user_ids.id for user_ids in users.values()]
            if user_id not in all_user_ids:
                abort(404)
            place_key = "Place." + place_id
            if place_key not in places:
                abort(404)
            body_request.update({"place_id": place_id})
            new_review = Review(**body_request)
            storage.new(new_review)
            storage.save()
            return jsonify(new_review.to_dict()), 201

    else:
        abort(501)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviewID(review_id):
    """Handel some HTTP methods that i am too tired to about now"""
    reviews = storage.all(Review)

    # USING HTTP GET
    if request.method == "GET":
        if not review_id:
            return jsonify([obj.to_dict() for obj in reviews.values()])
        key = "Review." + review_id
        try:
            return jsonify(reviews[key].to_dict())
        except KeyError:
            abort(404)
    
    # Using HTTP DELETE
    elif request.method == "DELETE":
        try:
            key = "Review." + review_id
            storage.delete(reviews[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # Using HTTP PUT
    elif request.method == "PUT":
        review_key = "Review." + review_id
        try:
            review = reviews[review_key]
        except KeyError:
            abort(404)
        if request.is_json:
            new = request.get_json()
        else:
            abort(400, "Not a JSON")
        for key, value in new.items():
            if key != "id" and key != "user_id" and key != "place_id" and\
               key != "created_at" and key != "updated_at":
                setattr(review, key, value)
            storage.save()
            return review.to_dict(), 200
    
    else:
        abort(501)
