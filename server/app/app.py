#!/usr/bin/python3
'''Flask app entry module'''

import pandas as pd
from flask import Flask, url_for, request, redirect, jsonify, flash, render_template
from flask_login import login_required
from models import storage
from views.student_views import student_views
from views.lecturer_views import lecturer_views
from views.admin_views import admin_views
from views import app_views, api
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import MySQLdb
from sqlalchemy.exc import IntegrityError
import os
from os import environ
import models
from models.student import Student
from models.lecturer import Lecturer
from models.course import Course


UPLOAD_FOLDER = 'uploads'
# Ensure the 'uploads' directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

# Register the blueprints
app.register_blueprint(student_views)
app.register_blueprint(lecturer_views)
app.register_blueprint(admin_views)

app.secret_key = "your_secret_key"  # Replace with your secret key

login_manager = LoginManager(app)  # Initialize LoginManager
student_login_manager = LoginManager(app)
lecturer_login_manager = LoginManager(app)

login_manager.login_view = "/login"  # Set the login view's name
student_login_manager.login_view = "student_login"  # Set the login view for students
lecturer_login_manager.login_view = "lecturer_login"  # Set the login view for lecturers

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    user = models.storage.get_session().query(
        Student).filter_by(id=user_id).first()
    if not user:
        user = models.storage.get_session().query(
            Lecturer).filter_by(id=user_id).first()
    return user

@student_login_manager.user_loader
def load_student(user_id):
    user = models.storage.get_session().query(
        Student).filter_by(id=user_id).first()
    return user

@lecturer_login_manager.user_loader
def load_lecturer(user_id):
    user = models.storage.get_session().query(
        Lecturer).filter_by(id=user_id).first()
    return user

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('admin/404.html')

@app.errorhandler(401)
def bad_request(error):
    flash(error, "danger")
    return render_template('admin/404.html')


@app.route('/')
def index():
    current_route = request.endpoint
    return render_template('index.html', current_route=current_route)


@app.route('/about')
def about():
    current_route = request.endpoint
    return render_template('about.html', current_route=current_route)


@app.route('/contact')
def contact():
    current_route = request.endpoint
    return render_template('contact.html', current_route=current_route)

@app.route('/events')
def events():
    current_route = request.endpoint
    return render_template('events.html', current_route=current_route)

@app.route('/news')
def news():
    current_route = request.endpoint
    return render_template('news.html', current_route=current_route)


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


@app.route("/student_login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        student = None
        student = models.storage.get_session().query(
            Student).filter_by(mat_number=username).first()
        
        if student and check_password_hash(student.password, password):
            login_user(student)
            return redirect(url_for("admin"))  # Redirect admin users
        else:
            flash("Login failed. Please check your credentials.", "danger")
            return render_template("admin/login.html")
    return render_template("admin/login.html")

@app.route("/lecturer_login", methods=["GET", "POST"])
def lecturer_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        lecturer = None
        lecturer = models.storage.get_session().query(
            Lecturer).filter_by(mat_number=username).first()
        
        if lecturer and check_password_hash(lecturer.password, password):
            login_user(lecturer)
            return redirect(url_for("admin"))  # Redirect admin users
        else:
            flash("Login failed. Please check your credentials.", "danger")
            return render_template("admin/login.html")
    return render_template("admin/login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        student = None
        student = models.storage.get_session().query(
            Student).filter_by(mat_number=username).first()
        lecturer = models.storage.get_session().query(
            Lecturer).filter_by(username=username).first()
        if student and check_password_hash(student.password, password):
            login_user(student)
            return redirect(url_for("admin_views.admin"))  # Redirect admin_views.admin users
        elif lecturer and check_password_hash(lecturer.password, password):
            login_user(lecturer)
            return redirect(url_for("admin_views.admin"))  # Redirect admin users
        else:
            flash("Login failed. Please check your credentials.", "danger")
            return render_template("admin/login.html")
    return render_template("admin/login.html")




@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Logout route for students
@app.route("/student_logout")
@login_required
def student_logout():
    logout_user()  # Log the student out using the student login manager
    return redirect(url_for("student_login"))  # Redirect to the student login page

# Logout route for lecturers
@app.route("/lecturer_logout")
@login_required
def lecturer_logout():
    logout_user()  # Log the lecturer out using the lecturer login manager
    return redirect(url_for("lecturer_login"))  # Redirect to the lecturer login page


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, debug=True, threaded=True)