from flask_app.controllers import users, welcomes, exercises, workout_sessions

from flask_app import app

if __name__ == "__main__":
    app.run(debug = True)