#!/usr/bin/python3
"""endpoint"""
import models
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """teardown to app"""
    models.storage.close()
