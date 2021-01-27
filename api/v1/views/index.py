#!/usr/bin/python3
"""Index file to views"""
from api.v1.views import app_views
from flask import jsonify



@app_views.route('/status')
def status():
    """Status route of API v1"""
    d = {"status": "OK"}
    return jsonify(d)
