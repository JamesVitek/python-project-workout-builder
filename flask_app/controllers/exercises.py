from flask import Flask, render_template, redirect, request, session
from flask_app.models.exercise import Exercise
from flask_app.models.user import User
from flask_app.models.workout_session import Workout_Session 

from flask_app import app

@app.route('/add_workout', methods = ["post"])
def create_exercise():
    Exercise.new_exercise(request.form)
    return redirect("/")

@app.route("/muscle_group/<type>")
def show_muscle_Group(type):
    session["type"] = type
    if "user_id" in session:
        query_data = {
                "user_id" : session["user_id"]
            }
        current_user = User.get_by_id(query_data)

        muscle_group = Exercise.get_workouts_by_type({'type': type})

        return render_template("muscle_group.html", muscle_group = muscle_group, current_user = current_user)
    
    muscle_group = Exercise.get_workouts_by_type({'type': type})

    return render_template("muscle_group.html", muscle_group = muscle_group)