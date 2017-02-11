from flask import Blueprint, render_template
from peewee import DoesNotExist
from math import ceil

from ..models import Post

blue = Blueprint('post', __name__)


@blue.route("/posts")
@blue.route("/post/<int:page_number>")
def posts(page_number=1):
    number_of_posts_per_page = 10
    number_of_total_posts = Post.select().where(Post.visible).count()
    number_of_pages = ceil(number_of_total_posts / number_of_posts_per_page)
    posts = Post.select().where(Post.visible).order_by(
        Post.post_date.desc()).paginate(page_number, number_of_posts_per_page)
    if number_of_pages <= 1:
        next_page = None
        previous_page = None
    elif page_number == 1 or number_of_pages > 1:
        next_page = None
        previous_page = page_number + 1
    elif number_of_pages > 1:
        if page_number < number_of_pages:
            next_page = page_number - 1
            previous_page = page_number + 1
        elif page_number > 1 and page_number == number_of_pages:
            next_page = page_number - 1
            previous_page = None
    else:
        return render_template('page_not_found.html'), 404

    return render_template("post/post_overview.html",
                           posts=posts,
                           next_page=next_page,
                           previous_page=previous_page,
                           number_of_pages=number_of_pages)


@blue.route("/post/<int:post_id>")
@blue.route("/post/<int:post_id>/<string:slug>")
def single_post(post_id, slug=None):
    try:
        post = Post.get((Post.id == post_id) & Post.visible)
    except DoesNotExist:
        return render_template('page_not_found.html'), 404
        return render_template('page_not_found.html'), 404
    return render_template("post/post.html", post=post)
