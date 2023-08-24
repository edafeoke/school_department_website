#!/usr/bin/python3
'''Flask app entry module'''

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
import MySQLdb
from sqlalchemy.exc import IntegrityError
import os
from os import environ
# from flask_restplus import Api
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
app.secret_key = "your_secret_key"  # Replace with your secret key

login_manager = LoginManager(app)  # Initialize LoginManager
login_manager.login_view = "/login"  # Set the login view's name
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

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('404.html')

@app.errorhandler(401)
def not_found(error):
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template('404.html')


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


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin/index.html')

@app.route('/admin/students', methods=['GET'])
@login_required
def all_students():
    students = storage.all(Student)
    return render_template('admin/students.html', students=students.values())

@app.route('/admin/lecturers', methods=['GET', 'POST'])
def all_lecturers():
    if request.method == 'GET':
        lecturers = storage.all(Lecturer)
        print(lecturers)
        return render_template('admin/lecturers.html', lecturers=lecturers.values())
    return render_template('admin/lecturers.html')

@app.route('/admin/courses', methods=['GET', 'POST'])
def all_courses():
    '''Returns lists of all courses'''

    if request.method == 'GET':
        courses = models.storage.get_session().query(
            Course).join(Lecturer).all()
        # courses = storage.all(Course)
        return render_template('admin/courses.html', courses=courses)
    return render_template('admin/courses.html')

@app.route('/admin/student/new', methods=['GET', 'POST'])
@login_required
def new_student():
    if request.method == 'POST':
        # Create a new student record using SQLAlchemy
        new_student = Student(**(dict(request.form)))
        new_student.hash_password("password")
        new_student.save()
        flash('Student record added successfully', "success")
        return redirect(url_for('all_students'))
    return render_template('admin/new_student.html')


@app.route('/admin/student/from_csv', methods=['GET', 'POST'])
@login_required
def new_students_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', "danger")
            return render_template('admin/new_student_from_csv.html')

        if file:
            file.save(os.path.join('uploads', file.filename))
            csv_path = os.path.join('uploads', file.filename)

            try:
                # Read CSV using Pandas
                df = pd.read_csv(csv_path)
                headers = df.columns.tolist()
                rows = df.values.tolist()
                uploaded_data = {'headers': headers, 'rows': rows}
                for row in rows:
                    new_student = {}
                    for index, header in enumerate(headers):
                        new_student[header] = row[index]
                    Student(**new_student).save()
                    flash('Student record added successfully', "success")
                return render_template('admin/new_student_from_csv.html', uploaded_data=uploaded_data)
            except IntegrityError as e:
                if isinstance(e.orig, MySQLdb.IntegrityError) and 'Duplicate entry' in str(e.orig):
                    duplicate_entry_message = "The provided mat number already exists."
                    flash(duplicate_entry_message, "danger")
                    return render_template('admin/new_student_from_csv.html')
                else:
                    return render_template('admin/new_student_from_csv.html')
            except Exception as e:
                flash(str(e), "danger")
                return render_template('admin/new_student_from_csv.html')
                # return jsonify({'error': 'Error reading CSV: ' + str(e)})
    return render_template('admin/new_student_from_csv.html')


@app.route('/admin/lecturer/new', methods=['GET', 'POST'])
@login_required
def new_lecturer():
    if request.method == 'POST':
        # Create a new lecturer record using SQLAlchemy
        new_lecturer = Lecturer(**(dict(request.form)))
        new_lecturer.hash_password("password")
        new_lecturer.save()
        flash("Lecturer registered successfully", "success")
        return redirect(url_for('all_lecturers'))
    return render_template('admin/new_lecturer.html')

@app.route('/admin/course/new', methods=['GET', 'POST'])
@login_required
def new_course():
    if request.method == 'POST':
        # Create a new course record using SQLAlchemy
        lecturer = models.storage.get_session().query(
            Lecturer).filter_by(id=request.form['lecturer']).first()
        # new_course = Course(**(dict(request.form)))
        new_course = Course()
        new_course.lecturer_id = lecturer.id
        new_course.title = request.form['title']
        new_course.code = request.form['code']
        new_course.save()
        flash("Course registered successfully", "success")
        return redirect(url_for('all_courses'))
    lecturers = storage.all(Lecturer)
    return render_template('admin/new_course.html', lecturers=lecturers.values())


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
        student = models.storage.get_session().query(
            Student).filter_by(mat_number=username).first()
        lecturer = models.storage.get_session().query(
            Lecturer).filter_by(username=username).first()
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


@app.route("/admin/students/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_student(id):
    student = models.storage.get_session().query(Student).filter_by(id=id).first()
    return redirect("admin/students.html")


@app.route("/admin/lecturers/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_lecturer(id):
    lecturer = models.storage.get_session().query(Lecturer).filter_by(id=id).first()
    return redirect("admin/lecturers.html")

@app.route("/admin/courses/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_course(id):
    course = models.storage.get_session().query(Course).filter_by(id=id).first()
    return redirect("admin/courses.html")


@app.route("/admin/students/delete?id=<id>", methods=["GET", "POST"])
@login_required
def delete_student(id):
    student = models.storage.get_session().query(Student).filter_by(id=id).first()
    storage.get_session().delete(student)
    storage.get_session().commit()
    flash('Student record successfully deleted', "success")
    return redirect(url_for("all_students"))


@app.route("/admin/lecturers/delete?id=<id>", methods=["GET", "POST"])
@login_required
def delete_lecturer(id):
    '''deletes a lecturer account'''
    lecturer = models.storage.get_session().query(Lecturer).filter_by(id=id).first()
    if lecturer:
        storage.get_session().delete(lecturer)
        storage.get_session().commit()
        flash('Lecturer record successfully deleted', "success")
    return redirect(url_for("all_lecturers"))

@app.route("/admin/courses/delete?id=<id>", methods=["GET", "POST"])
@login_required
def delete_course(id):
    '''deletes a course'''
    course = models.storage.get_session().query(Course).filter_by(id=id).first()
    if course:
        storage.get_session().delete(course)
        storage.get_session().commit()
        flash('Course record successfully deleted', "success")
    return redirect(url_for("all_courses"))


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
