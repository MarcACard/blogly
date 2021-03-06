"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "SUPER-DUPER-SECRET"
# debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def index():
    """Home Page"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5)

    return render_template("index.html", posts=posts)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


######################
# === User Routes ===
######################


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
    # TODO: get all user posts
    posts = Post.query.filter_by(user_id=user_id).all()
    if user == None:
        flash(f"User_id [{user_id}] does not exist.", "error")
        return redirect("/users")

    return render_template("user_details.html", user=user, posts=posts)


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


#####################
# === Post Routes ===
#####################


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Display a form to enable to a users to submit a post."""
    # TODO: Create Template for Route
    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template("post_new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """Process a new post form submission"""
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist("tag", int)
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f"New Post Added: {title}", "message")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """Display a specified post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template("post_detail.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Open a form to enable a user to edit a post."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("post_edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Process a form submission for post edits"""
    post = Post.query.get(post_id)

    # TODO: Validate Form Inputs
    new_title = request.form["title"]
    new_content = request.form["content"]
    tag_ids = request.form.getlist("tag", int)
    new_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    if post is None:
        flash(f"Attempted Changes Failed. Post {post_id} not found.", "error")
        return redirect("/")

    post.title = new_title
    post.content = new_content
    post.tags = new_tags

    db.session.add(post)
    db.session.commit()

    flash("Post Update Completed", "message")

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post from the database."""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("Post has been deleted.", "warning")

    return redirect(f"/users/{post.user_id}")


####################
# === Tag Routes ===
####################


@app.route("/tags")
def get_tags():
    """Show all tags on blog."""

    tags = Tag.query.all()
    return render_template("tag_list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def get_tag(tag_id):
    """Show a tag and all posts with the Tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("tag_post_list.html", tag=tag, posts=posts)


@app.route("/tags/new")
def new_tag():
    """display a form to create a new Tag"""
    return render_template("tag_add.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Process a new Tag if it doesn't already exist."""

    tag_name = request.form["tag"].title()

    if Tag.query.filter_by(name=tag_name).first() != None:
        flash(f'Tag: "{tag_name}" already exists.', "error")
        return redirect("/tags/new")

    tag = Tag(name=tag_name)

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag: {tag_name.title()} was created", "message")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Display a form for a users to edit a tag"""
    tag = Tag.query.get(tag_id)

    if tag is None:
        flash(f"Unable to find tag with ID: {tag_id}.", "error")
        return redirect("/tags")

    return render_template("tag_edit.html", tag=tag)


# ?: Is there a recommended method to structure functions for multiple checks? My structure below prevents excessive nesting, but uncertain if there is a 'preferred' way to setup a route.
@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def update_tag(tag_id):
    """Process a tag update."""
    tag = Tag.query.get(tag_id)

    if tag is None:
        flash(f"Attempted Changes Failed. Tag ID: {tag_id} not found.", "error")
        return redirect("/tags")

    tag_name = request.form["tag"].title()

    if Tag.query.filter_by(name=tag_name).first() != None:
        flash(f'Tag: "{tag_name}" already exists.', "error")
        return redirect(f"/tags/{tag_id}/edit")

    tag.name = tag_name

    db.session.add(tag)
    db.session.commit()

    flash("Tag Update Complete", "message")

    return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash("Tag has been deleted.", "warning")

    return redirect(f"/tags")
