from flask import Blueprint, render_template, jsonify, request
from controllers.student_controller import get_all_students

student_view = Blueprint('student_view', __name__)

@student_view.route('/students', methods=['GET'])
def student_list():
    students = get_all_students()
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'students': students})
    else:
        return render_template('index.html', students=students)
