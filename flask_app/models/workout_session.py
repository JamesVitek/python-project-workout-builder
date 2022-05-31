from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import exercise

class Workout_Session():
    
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.reps = data["reps"]
        self.sets = data["sets"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.exercise = {}

    @classmethod
    def build_workout_session(cls, data):
        query = "INSERT INTO workouts_schema.sessions (name, type, sets, reps, created_at, workout_id, user_id) VALUES (%(name)s, %(type)s, %(sets)s, %(reps)s, NOW(), %(workout_id)s, %(user_id)s);"

        result = connectToMySQL("workouts_schema").query_db(query, data)

        return result

    @classmethod
    def get_workouts_session(cls):
        query = "SELECT * FROM workouts_schema.sessions join workouts_schema.workouts where workout_id = workouts.id;"

        results = connectToMySQL("workouts_schema").query_db(query)

        session_with_images = []

        for row in results:
            workout = cls(row)
            session_info = {
                'id' : row['id'],
                'name' : row['name'],
                'type' : row['type'],
                'image' : row["image"],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            workout.exercise = exercise.Exercise(session_info)
            session_with_images.append(workout)
        return session_with_images

    @classmethod
    def clear_workout_session(cls):
        query = "delete from workouts_schema.sessions where id;"

        result = connectToMySQL("workouts_schema").query_db(query)

        return result

    @classmethod
    def remove_exercise(cls, data):
        query = "delete from workouts_schema.sessions where id = %(id)s;"

        result = connectToMySQL("workouts_schema").query_db(query, data)

        return result