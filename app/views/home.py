from flask import Blueprint, render_template, session, abort
from math import ceil

from ..models import Post, db

blue = Blueprint('home', __name__)


@blue.route("/")
@blue.route("/<int:page_number>")
def index(page_number=1):
    number_of_posts_per_page = 10
    number_of_total_posts = Post.select().where(Post.visible).count()
    number_of_pages = ceil(number_of_total_posts / number_of_posts_per_page)
    posts = Post.select().where(Post.visible).order_by(
        Post.post_date.desc()).paginate(page_number, number_of_posts_per_page)
    if number_of_pages <= 1:
        next_page = None
        previous_page = None
    elif page_number == 1:
        next_page = None
        previous_page = page_number + 1
    elif number_of_pages > 1:
        if page_number == number_of_pages:
            next_page = page_number - 1
            previous_page = None
        elif page_number < number_of_pages:
            next_page = page_number - 1
            previous_page = page_number + 1
        else:
            return render_template('page_not_found.html'), 404
    else:
        return render_template('page_not_found.html'), 404

    return render_template("home/index.html",
                           posts=posts,
                           next_page=next_page,
                           previous_page=previous_page,
                           number_of_pages=number_of_pages)


@blue.route("/about")
def about():
    return render_template("home/about.html")


@blue.errorhandler(404)
def page_not_found(e):
    render_template('page_not_found.html'), 404


@blue.before_app_request
def before_request():
    session.permanent = True
    db.connect()


@blue.after_app_request
def after_request(response):
    db.close()
    return response
