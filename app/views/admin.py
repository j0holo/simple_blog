from flask import Blueprint, render_template, redirect, Markup, url_for
from flask import abort, request, flash, session

from datetime import datetime, timedelta
import html2text

from ..models import Post, User, db
from ..forms import LoginForm
from ..utils import login_required, auth_user, logout_user, filter_markdown

blue = Blueprint('admin', __name__, url_prefix='/admin')

@blue.route("/overview")
@login_required
def posts():
    posts = Post.select().order_by(Post.post_date.desc())
    return render_template("admin/post_overview.html", posts=posts)

@blue.route("/add", methods=['GET', 'POST'])
@login_required
def add_post():
    # TODO: Add possibility to add and/or update images
    """
    Idea for uploading multiple images:
    Upload multiple images an give each image an unique UUID which the user should use
    Save the UUIDs in the database and reverence from the database
    Will be difficult for the user, they need to hit preview or something like that
    to see which UUID they get.

    Another option is to prefix the images with the id of the post. Don't think that is the
    best idea, but better than the UUID option.

    Both ideas need to prefix the download folder: ../static/<the_image.png> when they
    get saved in the database.

    Maybe another idea is to preview the images with javascript and when uploaded save the
    images in static/<post_id/<image>. When changes are made to a post check if the
    images are changed, if so delete the images that are no longer used and save the knew
    ones. Maybe also delete the old images from the db that are no longer in use.

    Sources:
        https://stackoverflow.com/questions/14069421/show-an-image-preview-before-upload
        http://www.html5rocks.com/en/tutorials/file/dndfiles/
    """
    if request.method == 'POST':
        if request.form['submit'] == "preview":
            title = request.form['title']
            markdown = request.form['markdown_text']
            html = filter_markdown(markdown)

            return render_template("admin/add_post.html",
                                   html=Markup(html),
                                   markdown=markdown,
                                   title=title)
        if request.form['submit'] == "post":
            title = request.form['title']
            markdown = request.form['markdown_text']

            if title and markdown:
                text = filter_markdown(markdown)
                if Post.add_post(title, text):
                    flash("Added post successfully")
                    return redirect(url_for('.posts'))
                else:
                    return "The title already exist"
    else:
        return render_template("admin/add_post.html")

@blue.route("/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = None
    try:
        post = Post.get(Post.id == post_id)
    except Post.DoesNotExist:
        abort(404)

    if request.method == 'POST':
        # TODO: Change request.form methods to WTForms (priority)
        if request.form['submit'] == "preview":
            title = request.form['title']
            markdown = request.form['markdown_text']
            html = filter_markdown(markdown)
            return render_template("admin/update_post.html",
                                   title=title,
                                   markdown=markdown,
                                   html=Markup(html),
                                   post_id=post.id)

        if request.form['submit'] == "post":
            title = request.form['title']
            markdown = request.form['markdown_text']

            if title and markdown:
                text = filter_markdown(markdown)
                post.title = title
                post.text = text
                post.save()
                flash("Post was updated")
                return redirect(url_for('.posts'))

    title = post.title
    markdown = html2text.html2text(post.text)
    html = filter_markdown(markdown)
    return render_template("admin/update_post.html",
                           title=title,
                           markdown=markdown,
                           html=Markup(html),
                           post_id=post.id)

@blue.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    try:
        post = Post.get(Post.id == post_id)
        post.delete_instance()
    except Post.DoesNotExist:
        abort(404)

    return redirect(url_for('.posts'))

@blue.route("/visible/<int:post_id>")
@login_required
def switch_post_visibility(post_id):
    """Switch the visible boolean of the post object.

    Read the post.visible field form the post object and
    flip the value to change the visibility.

    :param post_id: id of the post object
    """
    try:
        post = Post.get(Post.id == post_id)
    except Post.DoesNotExist:
        abort(404)
    if post.visible:
        post.visible = False
        post.save()
    else:
        post.visible = True
        post.save()
    return redirect(url_for('.posts'))

@blue.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        if User.check_password(email, password):
            user = User.get(User.email == email)
            auth_user(user)
            flash('You are now logged in')
            return redirect(url_for('.posts'))
        else:
            flash('Username or password do not match!')

    return render_template('admin/login.html', form=form)


@blue.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.index'))
