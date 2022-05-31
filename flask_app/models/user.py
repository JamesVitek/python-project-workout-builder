from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

db = "workouts_schema"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def valid_regester(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First name must be filled in.")
            is_valid = False

        if len(user['last_name']) < 1:
            flash("Last name must be filled in.")
            is_valid = False

        if len(user['email']) < 1:
            flash("Email must be filled in.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False

        if len(user['password']) < 7:
            flash("Password must be more than 8 characters.")
            is_valid = False

        if not (user["password"] == user["pass_register"]):
            flash("Passwords must match.")
            is_valid = False

        return is_valid

    @classmethod
    def add_user(cls, data):
        query = "Insert into users (first_name, last_name, email, password, created_at) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now())"

        results = connectToMySQL(db).query_db(query, data)

        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def valid_user(data):
        is_valid = True
        user = User.get_by_email(data)

        if not user:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, data["password"]):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid