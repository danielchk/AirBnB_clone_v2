#!/usr/bin/python3
""" holds class Amenities"""
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities(amenity_id):
    """return the amenity without id"""
    am = [obj.to_dict() for obj in storage.all("Amenities").values()]
    return jsonify(am)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Return amenity by id"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """delete a object amenity by his id"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity(amenity_id):
    """upgrade an object amenity"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    obj = Amenity(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """update amenity obj"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    return jsonify(obj.to_dict())
