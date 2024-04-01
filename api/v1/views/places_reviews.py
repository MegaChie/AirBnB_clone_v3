#!/usr/bin/python3
"""API endpoint for the reviews object"""
from api.v1.views import app_views
from flask import jsonify as jsny, make_response, abort, request as req
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def getReivewList(place_id):
    """get list of Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsny([review.to_dict() for review in place.reviews])


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def newReview(place_id):
    """create new Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    revi = req.get_json()
    if not revi:
        abort(400, "Not a JSON")
    if 'uid' not in revi:
        abort(400, "Missing uid")
    uid = revi['uid']
    user = storage.get(User, uid)
    if not user:
        abort(404)
    if 'text' not in revi:
        abort(400, "Missing text")

    review = Review(**revi)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsny(review.to_dict()), 201)


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
        if k not in ['id', 'uid', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, value)
    storage.save()
    return make_response(jsny(review.to_dict()), 200)
