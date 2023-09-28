from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from xhtml2pdf import pisa
from flask_login import login_required, logout_user
from io import BytesIO
import models
from models import storage
from models.lecturer import Lecturer
from models.student import Student
from models.course import Course
import os
import pdfkit
# Import other necessary modules

admin_views = Blueprint('admin_views', __name__)

@admin_views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    models_count = {
        'students':len(storage.all(Student)),
        'lecturers':len(storage.all(Lecturer)),
        'courses':len(storage.all(Course)),
    }
    return render_template('admin/index.html', models=models_count)


@admin_views.route('/admin/students', methods=['GET'])
@login_required
def all_students():
    students = storage.all(Student)
    return render_template('admin/students.html', students=students.values())

@admin_views.route('/admin_profile')
@login_required
def admin_profile():
    # Add your admin profile route logic here
    pass

# Add more admin-specific routes as needed

@admin_views.route("/admin/students/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_student(id):
    student = models.storage.get_session().query(Student).filter_by(id=id).first()
    return redirect("admin/students.html")


@admin_views.route("/admin/lecturers/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_lecturer(id):
    lecturer = models.storage.get_session().query(Lecturer).filter_by(id=id).first()
    return redirect("admin/lecturers.html")

@admin_views.route("/admin/courses/modify?id=<id>", methods=["GET", "POST"])
@login_required
def modify_course(id):
    course = models.storage.get_session().query(Course).filter_by(id=id).first()
    return redirect("admin/courses.html")


@admin_views.route("/admin/students/delete?id=<id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_student(id):
    student = models.storage.get_session().query(Student).filter_by(id=id).first()
    storage.get_session().delete(student)
    storage.get_session().commit()
    flash('Student record successfully deleted', "success")
    return redirect(url_for("admin_views.all_students"))


@admin_views.route("/admin/lecturers/delete/userId=<userId>", methods=["GET", "POST","DELETE"])
@login_required
def delete_lecturer(userId):
    '''deletes a lecturer account'''
    # print(request.form)
    id = request.form['userId']
    print(">>>>>>>>>>>, ", userId)
    if not userId:
        flash('No userId specified', "warn")
        return redirect(url_for("admin_views.all_lecturers"))
    lecturer = models.storage.get_session().query(Lecturer).filter_by(id=userId).first()
    if lecturer:
        storage.get_session().delete(lecturer)
        storage.get_session().commit()
        flash('Lecturer record successfully deleted', "success")
    else:
        flash('Something went wrong', "danger")
    return redirect(url_for("admin_views.all_lecturers"))

@admin_views.route("/admin/courses/delete?id=<id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_course(id):
    '''deletes a course'''
    course = models.storage.get_session().query(Course).filter_by(id=id).first()
    if course:
        storage.get_session().delete(course)
        storage.get_session().commit()
        flash('Course record successfully deleted', "success")
    return redirect(url_for("all_courses"))


@admin_views.route('/admin/lecturers', methods=['GET', 'POST'])
def all_lecturers():
    if request.method == 'GET':
        lecturers = storage.all(Lecturer)
        print(lecturers)
        return render_template('admin/lecturers.html', lecturers=lecturers.values())
    return render_template('admin/lecturers.html')

@admin_views.route('/admin/courses', methods=['GET', 'POST'])
def all_courses():
    '''Returns lists of all courses'''

    if request.method == 'GET':
        courses = models.storage.get_session().query(
            Course).join(Lecturer).all()
        # courses = storage.all(Course)
        return render_template('admin/courses.html', courses=courses)
    return render_template('admin/courses.html')

@admin_views.route('/admin/student/new', methods=['GET', 'POST'])
@login_required
def new_student():
    if request.method == 'POST':
        # Create a new student record using SQLAlchemy
        new_student = Student(**(dict(request.form)))
        new_student.hash_password("password")
        new_student.save()
        flash('Student record added successfully', "success")
        return redirect(url_for('admin_views.all_students'))
    return render_template('admin/new_student.html')


@admin_views.route('/admin/student/from_csv', methods=['GET', 'POST'])
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


@admin_views.route('/admin/lecturer/new', methods=['GET', 'POST'])
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

@admin_views.route('/admin/course/new', methods=['GET', 'POST'])
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

@admin_views.route('/generate_pdf')
def generate_pdf():
    models_count = {
        'students':len(storage.all(Student)),
        'lecturers':len(storage.all(Lecturer)),
        'courses':len(storage.all(Course)),
    }
    
    # Render an HTML template to convert to PDF
    rendered_template = render_template('admin/index.html', models=models_count)

    # Create a BytesIO buffer to store the PDF data
    buffer = BytesIO()

    # Use pisa to generate the PDF from HTML
    pdf = pisa.CreatePDF(BytesIO(rendered_template.encode('utf-8')), buffer)

    if not pdf.err:
        # Move to the beginning of the buffer
        buffer.seek(0)

        # Create a Response object to send the PDF for download or display
        response = Response(buffer.read(), content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response

@admin_views.route('/admin_logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("login"))
