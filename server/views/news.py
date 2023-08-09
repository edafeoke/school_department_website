#!/usr/bin/python3
""" objects that handle all default RestFul API actions for News """

# import api

from models.news import News
from models.user import User
from models import storage
from views import api
from flask import abort, jsonify, request, make_response
from flask_restx import Resource, fields
# from api.v1.auth import token_required

@api.route('/news', strict_slashes=False)
class News1(Resource):
    def get(self):
        """ returns list of all news objects """
        all_newss = []
        news = storage.all(News).values()
        for news in news:
            d = news.to_dict()
            del d['_sa_instance_state']
            print(d)
            all_newss.append(d)
        return jsonify(all_newss)


@api.route('/users/<user_id>/news', strict_slashes=False)
# @api.doc(security='apikey')
class News2(Resource):
    resource_fields = api.model('news', {
        'title': fields.String,
        'isCompleted': fields.Boolean,
    })

    def get(self, user_id):
        """ returns list of all news objects """

        user = storage.get(User, user_id)
        if not user:
            abort(404)

        newss = []
        all_newss = storage.all(News).values()
        for news in all_newss:
            d = news.to_dict()
            del d['_sa_instance_state']
            if news.user_id == user_id:
                newss.append(d)
        return jsonify(newss)

    # @api.doc(params={'title': ''})
    # @api.marshal_with(resource_fields, as_list=True)
    @api.expect(resource_fields)
    def post(self, user_id):
        """ Creates a news objects """
        data = request.get_json()
        if not data:
            abort(404, 'Not a JSON')
        print(data)
        user = storage.get(User, user_id)
        if not user:
            abort(404)

        news = News(data)
        news.user_id = user_id
        for k, v in data.items():
            setattr(news, k, v)
        news.save()
        t = news.to_dict()
        del t['_sa_instance_state']
        print(t)
        return make_response(jsonify(t), 201)


@api.route('/news/<news_id>', strict_slashes=False)
class News3(Resource):
    resource_fields = api.model('news', {
        'title': fields.String,
        'isCompleted': fields.Boolean,
    })
    def get(self, news_id):
        """ returns list of all news objects """
        news = storage.get(News, news_id)

        if not news:
            abort(404)

        t = news.to_dict()
        del t['_sa_instance_state']
        print(t)
        return jsonify(t)

    def delete(self, news_id):
        """ delete a news object """
        news = storage.get(News, news_id)

        if not news:
            abort(404)

        news.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    
    @api.expect(resource_fields)
    def put(self, news_id):
        """ Updates a news object """
        news = storage.get(News, news_id)

        if not news:
            abort(404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({"error": "Not a valid JSON"}), 400)

        for k, v in data.items():
            if k != 'id' and k != 'user_id' and k != 'created_at' and k != 'updated_at':
                setattr(news, k, v)
        news.save()
        t = news.to_dict()
        del t['_sa_instance_state']

        return make_response(jsonify(t), 203)
