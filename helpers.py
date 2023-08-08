import datetime

# from flask import Flask, flash, redirect, render_template, request, session
from flask import redirect, render_template, session
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os
from app import app


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# upload image and return the path
def image_url(type="post", image=""):
    # /workspaces/20566958/project
    APP_ROOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)))

    # add date to image name to make it unique
    # dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f') millisec = dt_obj.timestamp() * 1000
    time_in_milli = datetime.now().timestamp() * 1000
    image_name = str(int(time_in_milli)) + " " + image.filename

    if type == "post":
        # app.config["POSTS_UPLOAD_FOLDER"] ==> "static/images/posts"
        image_url = os.path.join(
            APP_ROOT_PATH, app.config["POSTS_UPLOAD_FOLDER"], secure_filename(image_name)
        )
        # save it in the upload server
        image.save(
            image_url
        )  # /workspaces/20566958/project/static/images/users/filename.jpg
        # get image url without root folder path
        image_short_url = os.path.join(
            app.config["POSTS_UPLOAD_FOLDER"], secure_filename(image_name)
        )
        return image_short_url   # static/images/users/filename.jpg
    elif type == "user":
        # app.config["USERS_UPLOAD_FOLDER"] ==> "static/images/users"
        image_url = os.path.join(
            APP_ROOT_PATH, app.config["USERS_UPLOAD_FOLDER"], secure_filename(image_name)
        )
        # save it in the upload server
        image.save(
            image_url
        )  # /workspaces/20566958/project/static/images/users/filename.jpg

        # get image url without root folder path
        image_short_url = os.path.join(
            app.config["USERS_UPLOAD_FOLDER"], secure_filename(image_name)
        )
        return image_short_url   # static/images/posts/filename.jpg
