#!/usr/bin/python3
'''rest api entry module'''

import pandas as pd
from flask import Flask, url_for, request, redirect, Response, flash
from flask_login import login_required
from models import storage
from views import app_views, api
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os
from os import environ
# from flask_restplus import Api
from models.student import Student
from models.lecturer import Lecturer
import models



UPLOAD_FOLDER = 'uploads'
# Ensure the 'uploads' directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
app.secret_key = "your_secret_key"  # Replace with your secret key

login_manager = LoginManager(app)  # Initialize LoginManager
login_manager.login_view = "/login"  # Set the login view's name
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = models.storage.get_session().query(Student).filter_by(id=user_id).first()
    if not user:
        user = models.storage.get_session().query(Lecturer).filter_by(id=user_id).first()
    return user

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
@login_required
def admin():
    return render_template('admin/index.html')


@app.route('/admin/students', methods=['GET', 'POST'])
@login_required
def all_students():
    if request.method == 'GET':
        students = storage.all(Student)
        print(students)
        return render_template('admin/students.html', students=students.values())
    return render_template('admin/students.html')

@app.route('/admin/lecturers', methods=['GET', 'POST'])
def all_lecturers():
    if request.method == 'GET':
        lecturers = storage.all(Lecturer)
        print(lecturers)
        return render_template('admin/lecturers.html', lecturers=lecturers.values())
    return render_template('admin/lecturers.html')


@app.route('/admin/student/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        # Create a new student record using SQLAlchemy
        new_student = Student(**(dict(request.form)))
        new_student.hash_password("password")
        new_student.save()
        return redirect(url_for('all_students'))
    return render_template('admin/new_student.html')


@app.route('/admin/student/from_csv', methods=['GET', 'POST'])
def new_students_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            file.save(os.path.join('uploads', file.filename))
            csv_path = os.path.join('uploads', file.filename)

            try:
                # Read CSV using Pandas
                df = pd.read_csv(csv_path)
                headers = df.columns.tolist()
                rows = df.values.tolist()
                uploaded_data = {'headers': headers, 'rows': rows}
                # return jsonify({'success': True, 'uploaded_data': uploaded_data})
                for row in rows:
                    new_student = {}
                    for index, header in enumerate(headers):
                        new_student[header] = row[index]
                    Student(**new_student).save()
                return render_template('admin/new_student_from_csv.html', uploaded_data=uploaded_data)
            except Exception as e:
                return jsonify({'error': 'Error reading CSV: ' + str(e)})

    return render_template('admin/new_student_from_csv.html')


@app.route('/admin/lecturer/new', methods=['GET', 'POST'])
def new_lecturer():
    return render_template('admin/ui-card.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({'success': 'File uploaded successfully'})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # students = models.storage.get_session().query.all(Student)
        student = None
        student = models.storage.get_session().query(Student).filter_by(mat_number=username).first()
        # for s in students:
        #     print(s)
        #     if s['mat_number'] == username:
        #         student = Student(**dict(s))
        #         break

        # lecturer = None
        # lecturer = models.storage.get_session().query(Lecturer).filter_by(mat_number=username).first()
        # for l in lecturers:
        #     if l.username == username:
        #         lecturer = l
        #         break
        # student = Student.query.filter_by(username=username).first()
        # lecturer = models.lecturer.Lecturer.query.filter_by(username=username).first()
        lecturer = models.storage.get_session().query(Lecturer).filter_by(username=username).first()
        if student and check_password_hash(student.password, password):
            login_user(student)
            return redirect(url_for("admin"))  # Redirect admin users
        elif lecturer and check_password_hash(lecturer.password, password):
            login_user(lecturer)
            return redirect(url_for("admin"))  # Redirect admin users
        else:
            flash("Login failed. Please check your credentials.", "danger")
            return render_template("admin/login.html")
    return render_template("admin/login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)
