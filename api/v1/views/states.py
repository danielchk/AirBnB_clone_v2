#!/usr/bin/python3
import models
from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, request, make_response

""" holds class State"""
@app_views.route('/states', methods=['GET'])
def get():
    """Return the objects without his id"""
    l = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(l)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_by_id(state_id):
    """Return the objects with his id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    """Delete with the id info"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app_views.route('/states', methods=['POST'])
def create():
    """Create a state object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    obj = State(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id):
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
