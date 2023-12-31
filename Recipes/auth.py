from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .model import User
import flask_login

bp = Blueprint("auth", __name__)


@bp.route("/signup")
def signup():
    """
    Display the signup page.
    """
    return render_template("auth/signup.html")


@bp.route("/login")
def login():
    """
    Display the login page.
    """
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    """
    Handle the login form submission.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if the user exists in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Sorry, the username is not correct. Please, signup in case you don't have any account.", "login_error")
        return redirect(url_for("auth.login"))
    
    # Check if the hashed password matches
    if user and user.check_password(password):
        flask_login.login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Sorry, the password is not correct.", "login_error")
        return redirect(url_for("auth.login"))
    

@bp.route("/signup", methods=["POST"])
def signup_post():
    """
    Handle the signup form submission.
    """
    email = request.form.get("email")
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Sorry, passwords are different")
        return redirect(url_for("auth.signup"))

    # Check if the email is already in the database
    if User.query.filter_by(email=email).first():
        flash("Sorry, the email you provided is already registered.", "signup_error")
        return redirect(url_for("auth.signup"))

    # Check if the username is already in the database
    if User.query.filter_by(username=username).first():
        flash("Sorry, the username you provided is already registered.", "signup_error")
        return redirect(url_for("auth.signup"))

    # Create a new user instance
    new_user = User(email=email, name=name, username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flask_login.login_user(new_user)
    return redirect(url_for("main.index"))


@bp.route('/logout')
def logout():
    """
    Log out the current user.
    """
    flask_login.logout_user()
    return redirect(url_for('auth.login'))