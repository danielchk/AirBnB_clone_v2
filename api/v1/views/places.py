#!/usr/bin/python3
"""State rule module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete place with id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """create place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    if "user_id" not in data:
        return make_response("Missing user_id", 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if "name" not in data:
        return make_response("Missing name", 400)
    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def get_places_search():
    """Get a list with all places"""
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    places = []
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if states == [] and cities == [] and amenities == []:
        for place in storage.all(Place).values():
            places.append(place.to_dict())
        return jsonify(places)
    if states != []:
        for state_id in data['states']:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    for place in city.places:
                        places.append(place.to_dict())
    if cities != []:
        for city_id in data['cities']:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    places.append(place.to_dict())
    return jsonify(places)
