from flask import render_template, request, session, redirect
from app import app
from db import select, insert
from datetime import datetime
from helpers import apology


@app.route("/")
def index():
    """Show latest blog posts"""
    return render_template(
        "index.html",
        posts=select("posts"),
        cats=select("cats", limit=10),
    )


@app.route("/post", methods=["GET", "POST"])
def post():
    """Show single post and posting comments"""
    if request.method == "POST":
        c_text = request.form.get("c_text")
        if not c_text:
            return apology("Comment text is required!")
        post_id = request.args.get("id")
        user_id = session["user_id"]
        published = 1
        createdAt = datetime.now()
        insert(
            "comments",
            post_id=post_id,
            user_id=user_id,
            text=c_text,
            published=published,
            createdAt=createdAt,
        )

        return redirect(f"{request.referrer}")
    else:
        post_id = request.args.get("id")
        show_post = select(table="posts", post_id=post_id)
        posts = select("posts", limit=10)
        cats = select("cats", limit=10)
        user = select("users", user_id=show_post[0]["author_id"])
        comments = select("comments", post_id=post_id)
        comments_count = len(comments)
        return render_template(
            "post.html",
            show_post=show_post[0],
            posts=posts,
            user=user[0],
            cats=cats,
            comments=comments,
            comments_count=comments_count
        )


@app.route("/category")
def category():
    """Show latest category posts"""
    cat_id = request.args.get("id")
    posts = select("posts", cat_id=cat_id)
    posts_cat = select("cats", cat_id=cat_id)

    return render_template(
        "category.html",
        posts=posts,
        posts_cat=posts_cat[0],
        cats=select("cats", limit=10),
    )
