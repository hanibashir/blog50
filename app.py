from flask import Flask, session, g
from flask_session import Session
# from flask_ckeditor import CKEditor
# from flask_ckeditor import CKEditorField
# from wtforms import StringField, SubmitField

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# # The maximum number of items the session stores
# # before it starts deleting some, default 500
# app.config['SESSION_FILE_THRESHOLD'] = 100
Session(app)
# ckeditor = CKEditor(app)
app.config["IMAGES_UPLOAD_FOLDER"] = "static/images"
app.config["POSTS_UPLOAD_FOLDER"] = "static/images/posts"
app.config["USERS_UPLOAD_FOLDER"] = "static/images/users"

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id is not None:
        g.user = session["user_id"]
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


import views.dashboard
import views.user
import views.blog
