from flask_app.config.mysqlconnection import connectToMySQL

class Exercise():
    
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.image = data["image"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_workouts_by_type(cls, data):
        query = "SELECT * FROM workouts_schema.workouts where type = %(type)s;"

        results = connectToMySQL("workouts_schema").query_db(query, data)

        workouts = []

        for row in results:
            workouts.append(Exercise(row))

        return workouts

    @classmethod
    def new_exercise(cls, data):
        query = "INSERT INTO workouts_schema.workouts (name, type, created_at) VALUES (%(name)s, %(type)s, NOW());"

        result = connectToMySQL("workouts_schema").query_db(query, data)

        return result

    @classmethod
    def get_workout_by_id(cls, data):
        query = "SELECT * FROM workouts_schema.workouts where id = %(id)s;"

        result = connectToMySQL("workouts_schema").query_db(query, data)

        return cls(result[0])