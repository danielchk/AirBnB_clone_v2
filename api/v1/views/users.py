#!/usr/bin/python3
""" holds class City"""
from models import storage
from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_all_user():
    """return user without id"""
    us = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(us)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_id_user(user_id):
    """get user by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """delete user by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return make_response(jsonify({}), 200)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """create name to user"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    obj = User(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates user """
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    return jsonify(obj.to_dict())
