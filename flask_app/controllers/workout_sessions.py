from flask import Flask, render_template, redirect, request, session
from flask_app.models.exercise import Exercise
from flask_app.models.user import User
from flask_app.models.workout_session import Workout_Session 

from flask_app import app

@app.route("/add_workout_to_plan/<int:id>", methods=["post"])
def create_workout_plan(id):

    workout = Exercise.get_workout_by_id({'id': id})

    exercise = {
        "name" : workout.name,
        "type" : workout.type,
        "sets" : request.form['sets'],
        "reps" : request.form['reps'],
        "workout_id" : id,
        "user_id" : session["user_id"]
    }

    Workout_Session.build_workout_session(exercise)
    return redirect("/muscle_group/" + exercise['type'])

@app.route("/workout_session")
def show_session():
    if "user_id" in session:
        query_data = {
                "user_id" : session["user_id"]
            }
        current_user = User.get_by_id(query_data)

        workouts = Workout_Session.get_workouts_session()

        return render_template("workout_session.html", workouts = workouts, current_user = current_user)
    
    workouts = Workout_Session.get_workouts_session()

    return render_template("workout_session.html", workouts = workouts)

@app.route("/clear_workout")
def clear_workout():
    Workout_Session.clear_workout_session()
    return redirect("/workout_session")

@app.route("/exercise/remove/<int:id>")
def remove_exercise(id):
    Workout_Session.remove_exercise({'id' : id})
    return redirect("/workout_session")