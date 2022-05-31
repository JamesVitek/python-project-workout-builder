from flask import session, render_template, redirect, request
from flask_app.models.user import User
from flask_app.models.exercise import Exercise
from flask_app.models.workout_session import Workout_Session
from flask_app import app
from flask import flash

@app.route("/")
def welcome():
    return render_template("welcome_page.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/logout")
def logout():
    session.clear()
    Workout_Session.clear_workout_session()
    return redirect("/")