# views/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin.index"))  # Redirect admin users
            elif user.role == "student":
                return redirect(url_for("student_view.students"))  # Redirect student users
        else:
            flash("Login failed. Please check your credentials.", "danger")
    
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
