#!/usr/bin/python3
"""API endpoint for the reviews object"""
from api.v1.views import app_views
from flask import jsonify as jsny, make_response, abort, request as req
import json
from os import getenv
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/searchedPlaces/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def reviewAPI(place_id):
    """
     - GET: Retrieves the list of all reviews if place ID is passed.
            Or a specific object if it is passed.
     - POST: Adds new object if a link exsists.
             Returns error code if other
    """
    fullRevw = storage.all(Review)
    fullPlac = storage.all(Place)

    # Using HTTP GET
    if req.method == "GET":
        seek = "Place." + place_id
        try:
            found = fullPlac[seek]
            data = []
            for name in found.fullRevw:
                entry = name.to_dict()
                data.append(entry)
            return jsny(data)
        except KeyError:
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
            foundUser = []
            for name in fullUser.values():
                entry = name.id
                foundUser.append(entry)
            if user_id not in foundUser:
                abort(404)
            seek = "Place." + place_id
            if seek not in fullPlac:
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    get place depend
    """
    reques = req.get_json()
    if reques is None:
        abort(400, "Not a JSON")
    if reques is None or (req.get('states') is None and
                       req.get('cities') is None and
                       req.get('amenities') is None
                      ):
        listPlaces = storage.all(Place)
        return jsny([place.to_dict() for place in listPlaces.values()])
    places = []
    if reques.get('states'):
        states = [storage.get("State", id) for id in reques.get('states')]
        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)
    if reques.get('cities'):
        cities = [storage.get("City", id) for id in reques.get('cities')]
        for c in cities:
            for p in c.places:
                if p not in places:
                    places.append(place)
    if not places:
        places = storage.all(Place)
        places = [p for p in places.values()]
    if reques.get('amenities'):
        listAmenity = [storage.get("Amenity", id) for id in reques.get('amenities')]
        currentPort = getenv('HBNB_API_PORT')
        port = 5000
        if currentPort:
            port = currentPort
        loopUrl = "http://0.0.0.0:{}/api/v1/places/".format(port)
        i = 0
        breakPoint = len(places)
        while i < breakPoint:
            place = places[i]
            url = loopUrl + '{}/amenities'
            req = url.format(place.id)
            res = req.get(req)
            amnityInpage = json.loads(res.text)
            amenities = [storage.get("Amenity", o['id']) for o in amnityInpage]
            for amenity in listAmenity:
                if amenity not in amenities:
                    places.pop(i)
                    breakPoint -= 1
                    i -= 1
                    break
            i += 1
    return jsny([place.to_dict() for place in places])
