from flask import flash, redirect, render_template, request, session
from app import app
from db import select, insert, update, delete
from helpers import apology, login_required, image_url
from slugify import slugify
from datetime import datetime
import os
from pathlib import Path


@app.route("/dashboard/", methods=["GET", "POST"])
@login_required
def dashboard():
    """Show main dashboard"""
    if request.method == "POST":
        delete_post = request.form.get("delete_post")
        delete_cat = request.form.get("delete_cat")

        # print(id_list[0])
        if delete_post:
            post_id = delete_post
            # delete post image from upload folder
            post_rows = select(
                "posts", no_cat="no_cat", post_id=post_id, user_id=session["user_id"]
            )
            try:
                os.remove(post_rows[0]["img_url"])
            except:
                pass
            # delete post
            delete("posts", post_id=post_id)
            flash("Post deleted!")
        # deleting category
        elif delete_cat:
            cat_id = delete_cat
            # select the associated posts
            posts = select("posts", cat_id=cat_id)
            # update the posts category_id set it to 0 before deleting the category
            for post in posts:
                update(
                    "posts",
                    cat_deleted="cat_deleted",
                    cat_id=0,
                    user_id=session["user_id"],
                    post_id=post["id"],
                )

            # delete category
            delete("cats", cat_id=cat_id)
            flash("Category deleted!")
        return redirect("/dashboard")
    else:
        # get the logged user posts
        posts = select("posts", user_id=session["user_id"])

        # check if any posts have category_id == 0
        posts_without_cat = select("posts", no_cat="no_cat", cat_id=0)
        # assign "No Category" to posts variable row named as category
        for i in range(len(posts_without_cat)):
            posts_without_cat[i]["category"] = "No Category"
        # add these posts to posts variable
        posts.extend(posts_without_cat)

        return render_template(
            "dashboard/index.html",
            posts=posts,
            cats=select("cats"),
        )


@app.route("/dashboard/new_post/", methods=["GET", "POST"])
@login_required
def new_post():
    """Add new post"""
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        cat_id = request.form.get("cat")
        if request.form.get("publish"):
            status = int(request.form.get("publish"))
        else:
            status = 0

        image = request.files["img"]

        # check if input fields empty submitted
        if not title:
            return apology("Post title is required!")
        if not content:
            return apology("Post content is required!")
        if not cat_id:
            return apology("Choose category!")
        if not image:
            return apology("Choose post image!")

        created_at = datetime.now()

        # prepare slug
        slug = slugify(title)

        # get image path
        img_short_url = image_url("post", image)

        # inser int posts table
        post_id = insert(
            "posts",
            user_id=session["user_id"],
            title=title,
            cat_id=cat_id,
            slug=slug,
            status=status,
            created_at=created_at,
            content=content,
            img_url=img_short_url,
        )
        flash("New post saved!")
        return redirect("/dashboard")

    else:
        return render_template("dashboard/new_post.html", cats=select("cats"))


# edit post
@app.route("/dashboard/post/", methods=["GET", "POST"])
@login_required
def edit_post():
    """Edit post"""
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        post_id = request.form.get("post_id")
        cat_id = request.form.get("cat")
        if request.form.get("publish"):
            status = int(request.form.get("publish"))
        else:
            status = 0

        # check if input fields empty submitted
        if not title:
            return apology("Post title is required!")
        if not content:
            return apology("Post content is required!")
        if not cat_id:
            return apology("Choose Category!")

        # prepare slug
        slug = slugify(title)

        image = request.files.get("img")
        # if changing the post image
        if image:
            img_short_url = image_url("post", image)
            # update post
            update(
                "posts",
                change_img="change_img",
                title=title,
                slug=slug,
                status=status,
                content=content,
                cat_id=cat_id,
                user_id=session["user_id"],
                post_id=post_id,
                img_short_url=img_short_url,
            )
            # delete the old image from upload folder
            try:
                os.remove(request.form.get("old_img_url"))
            except OSError:
                pass

        else:
            # update post
            update(
                "posts",
                title=title,
                slug=slug,
                status=status,
                content=content,
                cat_id=cat_id,
                user_id=session["user_id"],
                post_id=post_id,
            )
        flash("Post update saved!")
        return redirect("../")

    else:
        action = request.args.get("action")
        if action:
            if action == "edit":
                post_id = request.args.get("post_id")
                # if the post has no category
                post = []
                post_rows = select(
                    "posts",
                    no_cat="no_cat",
                    post_id=post_id,
                    user_id=session["user_id"],
                )
                if post_rows[0]["category_id"] == 0:
                    post = post_rows[0]
                else:
                    post_rows = select(
                        "posts", post_id=post_id, user_id=session["user_id"]
                    )
                    post = post_rows[0]

                return render_template(
                    "dashboard/edit_post.html",
                    cats=select("cats"),
                    post=post,
                )
            # elif action == "show":
            #     return render_template("/post.html", cats=cats, post=post[0])


# add category
@app.route("/dashboard/new_cat/", methods=["GET", "POST"])
@login_required
def new_cat():
    """Add new category"""
    if request.method == "POST":
        cat_title = request.form.get("cat_title").strip()
        cat_desc = request.form.get("cat_desc").strip()

        # check if input fields empty submitted
        if not cat_title:
            return apology("Category title is required!")

        if not cat_desc:
            cat_desc = "No description"

        # Query database to check if category already exists
        cat_rows = select("cats", title=cat_title)
        if len(cat_rows) > 0:
            return apology("Category already exists")

        # prepare slug
        slug = slugify(cat_title)

        # insert into category table
        insert("cats", cat_title=cat_title, cat_desc=cat_desc, slug=slug)
        flash("New category saved!")
        return redirect("/dashboard/")
    else:
        return render_template("dashboard/new_cat.html")


# edit category
# edit post
@app.route("/dashboard/cat/", methods=["GET", "POST"])
@login_required
def edit_cat():
    """Edit category"""
    if request.method == "POST":
        cat_title = request.form.get("cat_title").strip()
        cat_desc = request.form.get("cat_desc").strip()
        cat_id = request.form.get("cat_id")

        # check if input fields empty submitted
        if not cat_title:
            return apology("Category title is required!")

        if not cat_desc:
            cat_desc = "No description"

        # Query database to check if category already exists
        # cat_rows = select("cats", title=cat_title)
        # if len(cat_rows) > 0:
        #     return apology("Category already exists")

        # prepare slug
        slug = slugify(cat_title)

        # category category
        update("cats", cat_title=cat_title, cat_desc=cat_desc, slug=slug, cat_id=cat_id)
        flash("Category update saved!")
        return redirect("../")
    else:
        action = request.args.get("action")
        if action:
            if action == "edit":
                cat_id = request.args.get("cat_id")
                cat_rows = select("cats", cat_id=cat_id)
        return render_template("dashboard/edit_cat.html", cat=cat_rows[0])
