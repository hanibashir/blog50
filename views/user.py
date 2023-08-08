from app import app
from db import db, select, insert, update
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash, redirect, render_template, request, session
from helpers import image_url, apology
import os

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure email and password are not empty
        if not email or not password:
            return apology("Fill the email and password fields")

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], password
        ):
            return apology("invalid email and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("You were successfully logged in")
        # Redirect user to home page
        return redirect("/dashboard/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("user/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        pwConfirmation = request.form.get("confirm_password")

        # Ensure all required fields were submitted
        if not first_name or not last_name or not email or not password:
            return apology("fill all required fields")

        # check password confirmation
        if password != pwConfirmation:
            return apology("Passwords do NOT match", 400)


        # Query database for email to check if the user is aleardy exists
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(rows) > 0:
            return apology("Email already registered")

        image = request.files["img"]
        img_short_url = ""
        if not image:
            img_short_url = os.path.join(app.config["IMAGES_UPLOAD_FOLDER"], "user-blue-thumbnail.png")
        else:
            # get image path
            img_short_url = image_url("user", image)

        # convert password to hash
        pwHash = generate_password_hash(password)
        newUserId = insert(
            "users",
            first_name=first_name,
            last_name=last_name,
            email=email,
            pwHash=pwHash,
            img_short_url=img_short_url
        )
        session["user_id"] = newUserId
        flash("You were successfully registered!")
        return redirect("/dashboard/")
    return render_template("user/register.html")


@app.route("/user/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")
        about = request.form.get("about")

        user_id = session["user_id"]

        # Ensure all required fields were submitted
        if not first_name or not last_name:
            return apology("fill all required fields")

        image = request.files.get("img")
        print(image.filename)

        # changing password case
        if new_password:
            if new_password != confirm_new_password:
                return apology("The two new passwords do not match!")
            elif not old_password:
                return apology("Enter your old password")
            else:
                # Query database for user
                rows = select("users", user_id=user_id)

                # Ensure old password is correct
                if not check_password_hash(rows[0]["password_hash"], old_password):
                    return apology("invalid password")
                # convert password to hash
                pwHash = generate_password_hash(new_password)

                # changing password and image
                if image:
                    img_short_url = image_url("user", image)
                    update(
                        "users",
                        change_img="change_img",
                        first_name=first_name,
                        last_name=last_name,
                        pwHash=pwHash,
                        about=about,
                        user_id=user_id,
                        img_short_url=img_short_url
                    )
                    # delete the old image from upload folder
                    try:
                        old_image = request.form.get("old_img_url")
                        if old_image != "static/images/user-blue-thumbnail.png":
                            os.remove(old_image)
                    except OSError:
                        pass
                else:
                    # changing password only
                    update(
                        "users",
                        first_name=first_name,
                        last_name=last_name,
                        pwHash=pwHash,
                        about=about,
                        user_id=user_id,
                    )
                flash("Profile updated")
                return redirect("/dashboard")
        # changing the image but not password
        elif image:
            img_short_url = image_url("user", image)
            update(
                "users",
                change_img="change_img",
                first_name=first_name,
                last_name=last_name,
                about=about,
                user_id=user_id,
                img_short_url=img_short_url
            )
            # delete the old image from upload folder
            try:
                old_image = request.form.get("old_img_url")
                if old_image != "static/images/user-blue-thumbnail.png":
                    os.remove(old_image)
            except OSError:
                pass
            flash("Profile updated")
            return redirect("/dashboard")
        else:
            update(
                "users",
                first_name=first_name,
                last_name=last_name,
                about=about,
                user_id=user_id,
            )
            flash("Profile update saved")
            return redirect("/dashboard")
    else:
        user_row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        return render_template("user/profile.html", user=user_row[0])


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    # flash("Logged out!")
    return redirect("/")
