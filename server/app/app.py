#!/usr/bin/python3
'''rest api entry module'''

from flask import Flask, url_for, request
from models import storage
from views import app_views, api
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from os import environ
# from flask_restplus import Api
from models.student import Student


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
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('404.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/index.html')


@app.route('/admin/students', methods=['GET', 'POST'])
def all_students():
    if request.method == 'GET':
        students = storage.all(Student)
        print(students)
        return render_template('admin/students.html', students=students.values())
    return render_template('admin/students.html')


@app.route('/admin/student/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        student_object = {
            'name': request.form['name'],
            'password': 'password',
            'mat_number': request.form['mat_number'],
            'level': request.form['level'],
            'sex': request.form['sex'],
        }
        # Create a new student record using SQLAlchemy
        new_student = Student()
        new_student.name = request.form['name']
        new_student.password = 'password'
        new_student.mat_number = request.form['mat_number']
        new_student.level = request.form['level']
        new_student.sex = request.form['sex']
        print(new_student)
        storage.new(new_student)
        storage.save()
        return render_template('admin/students.html')
    return render_template('admin/new_student.html')


@app.route('/admin/lecturer/new', methods=['GET', 'POST'])
def new_lecturer():
    return render_template('admin/ui-card.html')


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
