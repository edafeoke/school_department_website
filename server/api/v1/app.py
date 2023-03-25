#!/usr/bin/python3
'''rest api entry module'''

from flask import Flask
from models import storage
from api.v1.views import app_views, api
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from os import environ
# from flask_restplus import Api


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# api = Api(app)

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
