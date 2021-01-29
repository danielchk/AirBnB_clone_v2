#!/usr/bin/python3
""" holds class State"""
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, abort, request, make_response

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Return the objects without his id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """Return the city with his id"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete city with the id info"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """Create a city object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    obj = City(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    """Updates state """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    return jsonify(obj.to_dict())
