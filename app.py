"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "SUPER-DUPER-SECRET"
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def index():
    """Home Page"""
    # TODO: Fix in later exercises
    flash("This is a test", "msg")
    return redirect("/users")


@app.route("/users")
def users_list():
    """Display a list of all users."""
    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route("/users/new")
def new_user():
    """New User Signup Form"""

    return render_template("user_form.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """Create a new user and redirect to user details page."""

    # TODO: Validate server-side before adding to DB
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    # TODO: Error handling
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash(f"New User Created: {first_name} {last_name}")
    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Display User Details."""
    user = User.query.get(user_id)

    if user == None:
        flash(f"User_id [{user_id}] does not exist.", "error")
        return redirect("/users")

    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def user_edit(user_id):
    """Display a form for the user to update their profile."""
    user = User.query.get(user_id)

    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_edit_save(user_id):
    """Process changes to a user profile."""
    # TODO: Save changes submitted by user.
    user = User.query.get(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    flash("User details updated.")
    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    """Delete a users profile"""
    # Todo: Delete provided user id
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User_id {user.id} deleted.")
    return redirect("/users")
