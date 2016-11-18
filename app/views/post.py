from flask import Blueprint, render_template, abort
from peewee import DoesNotExist

from ..models import Post

blue = Blueprint('post', __name__)


@blue.route("/posts")
def posts():
    posts = Post.select().where(Post.visible).order_by(
        Post.post_date.desc())
    return render_template("post/post_overview.html", posts=posts)


@blue.route("/post/<int:post_id>")
def single_post(post_id):
    try:
        post = Post.get((Post.id == post_id) & Post.visible)
    except DoesNotExist:
        return abort(404)
    return render_template("post/post.html", post=post)
