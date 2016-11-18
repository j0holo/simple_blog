from flask import Blueprint, render_template, session

from ..models import Post, db

blue = Blueprint('home', __name__)


@blue.route("/")
def index():
    posts = Post.select().where(Post.visible == True).order_by(
        Post.post_date.desc())
    return render_template("home/index.html", posts=posts)


@blue.route("/about")
def about():
    return render_template("home/about.html")


@blue.before_app_request
def before_request():
    session.permanent = True;
    db.connect()


@blue.after_app_request
def after_request(response):
    db.close()
    return response
