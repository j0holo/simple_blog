from flask import Blueprint, render_template
from ..models import Post, User, db

blue = Blueprint('post', __name__)

@blue.route("/posts")
def posts():
    # TODO: Create an overview of all posts
    posts = Post.select().order_by(Post.post_date.desc())
    return render_template("post/post_overview.html", posts=posts)

@blue.route("/post/<int:post_id>")
def single_post(post_id):
    post = Post.get(Post.id == post_id)
    return render_template("post/post.html", post=post)
