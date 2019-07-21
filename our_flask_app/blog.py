import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
)
from werkzeug.exceptions import abort

from our_flask_app.auth import login_required
from our_flask_app.db import get_db

# Creates a blueprint named `blog`
# Like the application object, this needs to know where it's
# defined, so we pass in __name__ as the second argument
# Unlike the 'auth' blueprint, blog does not have a url_prefix
# So the index will be at `/`, the `create` view at `/create`
# and so on
# >>> The blog is the main feature of our app, so it makes sense
# >>> that it's at the index
bp = Blueprint("blog", __name__)


# Associate the view with its blueprint using bp.route
# When Flask receives a request to /auth/register, it will call the
# register view and use the returned value as the response
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)" +
                " VALUES (?, ?, ?)",
                (title, body, g.user["id"])
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")

def get_post(id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username" +
        " FROM post p JOIN user u ON p.author_id = u.id" +
        " WHERE p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        # abort() will raise a special exception that returns a
        # HTTP status code. It takes an optional message to
        # show with the error, otherwise a default message is used
        # 404 == 'Not Found'
        # 403 = 'Forbidden'
        abort(404, f"Post id {id} doesn't exist.")

    # the `check_author` argument is defined so that the function
    # can be used to get a `post` without checking the author
    # This would be helpful if you wrote a view to show an individual
    # post on a page, where the user doesn't matter because they're
    # not modifying the post.
    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


# Unlike the views we've written so far, the `update` function
# takes an argument, `id`, which corresponds to the
# `<int:id>` in the route. Flask will capture the id, make sure
# it's an int and pass it as the id argument. If you don't
# specify `int:` and instead do `<id>`, it will be a string.
@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" +
                " WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
