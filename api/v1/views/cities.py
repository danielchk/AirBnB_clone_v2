#!/usr/bin/python3
""" holds class State"""
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Return the objects without his id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """Return the city with his id"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete city with the id info"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Create a city object"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    if "name" not in data:
        return make_response("Missing name", 400)
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates city """
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
