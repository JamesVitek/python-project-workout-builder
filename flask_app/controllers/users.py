from flask import session, render_template, redirect, request
from flask_app.models.user import User
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/register", methods=["post"])
def register():
    if not User.valid_regester(request.form):
        return redirect("/")

    encrypt_pass = bcrypt.generate_password_hash(request.form["password"])

    quere_data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : encrypt_pass
    }

    User.add_user(quere_data)

    logged_in = User.get_by_email(request.form)

    session["user_id"] = logged_in.id

    return redirect("/categories_page")

@app.route("/login", methods=["post"])
def login():
    if not User.valid_user(request.form):
        return redirect("/login_page")

    logged_in = User.get_by_email(request.form)

    session["user_id"] = logged_in.id

    return redirect("/categories_page")

@app.route("/categories_page")
def categories_page():
        if "user_id" not in session:
            flash("Please re-login to continue")
            return redirect("/")
        
        query_data = {
            "user_id" : session["user_id"]
        }

        current_user = User.get_by_id(query_data)

        return render_template("categories.html", current_user = current_user) #all_users = all_users