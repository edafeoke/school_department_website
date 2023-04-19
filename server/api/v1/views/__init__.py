#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint
from flask_restx import Api


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


api = Api(app_views,
          title="Computer science department website API docs",
          version='1.0')

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.todos import *
from api.v1.views.news import *

# from api.v1.views.places import *
# from api.v1.views.places_reviews import *
# from api.v1.views.cities import *