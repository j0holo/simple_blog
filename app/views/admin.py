import os

import html2text
from flask import Blueprint, render_template, redirect, Markup, \
    url_for, request, flash
from werkzeug.utils import secure_filename
from slugify import slugify

from app import app
from ..forms import LoginForm
from ..models.image import Image
from ..models.user import User
from ..models.post import Post
from ..site_logger import logger
from ..utils import login_required, auth_user, logout_user, allowed_file, \
    filter_markdown

blue = Blueprint('admin', __name__, url_prefix='/admin')


@blue.route("/overview")
@login_required
def posts():
    posts = Post.select().order_by(Post.post_date.desc())
    return render_template("admin/post_overview.html", posts=posts)


@blue.route("/add", methods=['GET', 'POST'])
@login_required
def add_post():
    """Upload a new post to the website

    :return: add_post.html
    """
    if request.method == 'POST':
        if request.form['submit'] == "preview":
            title = request.form['title']
            markdown_text = request.form['markdown_text']
            html = filter_markdown(markdown_text)

            return render_template("admin/add_post.html",
                                   html=Markup(html),
                                   markdown=markdown_text,
                                   title=title)
        if request.form['submit'] == "post":
            title = request.form['title']
            markdown_text = request.form['markdown_text']

            if title and markdown_text:
                html = filter_markdown(markdown_text)
                if Post.add_post(title, html):
                    flash("Added post successfully")
                    logger.info('A new post has been added: %s', title)
                    return redirect(url_for('.posts'))
                else:
                    flash("The title already exist")
                    return render_template("admin/add_post.html",
                                           html=html,
                                           markdown=markdown_text,
                                           title=title)
    else:
        return render_template("admin/add_post.html")


@blue.route("/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = None
    try:
        post = Post.get(Post.id == post_id)
    except Post.DoesNotExist:
        return render_template('page_not_found.html'), 404

    if request.method == 'POST':
        if request.form['submit'] == "preview":
            title = request.form['title']
            markdown_text = request.form['markdown_text']
            html = filter_markdown(markdown_text)
            return render_template("admin/update_post.html",
                                   title=title,
                                   markdown=markdown_text,
                                   html=Markup(html),
                                   post_id=post.id)

        if request.form['submit'] == "post":
            title = request.form['title']
            markdown_text = request.form['markdown_text']

            if title and markdown_text:
                text = filter_markdown(markdown_text)
                post.title = title
                post.slug = slugify(title)
                post.text = text
                post.save()
                flash("Post was updated")
                logger.info('Post %d has been updated', post_id)
                return redirect(url_for('.posts'))

    title = post.title
    markdown_text = html2text.html2text(post.text)
    html = filter_markdown(markdown_text)
    return render_template("admin/update_post.html",
                           title=title,
                           markdown=markdown_text,
                           html=Markup(html),
                           post_id=post.id)


@blue.route("/update-time/<int:post_id>")
@login_required
def update_post_date(post_id):
    """Update the post_date of a post.

    Usefull when you are not finished with your post
    and want to update the time when you make the post
    visible.

    :param post_id: id of the post.
    :return: redirect or 404
    """
    if Post.update_post_date(post_id):
        logger.info('post_date of %d has been updated', post_id)
        return redirect(url_for('.posts'))
    else:
        return render_template('page_not_found.html'), 404


@blue.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    """Delete a post

    :param post_id: id of the post object
    :return: redirect or 404
    """
    if Post.delete_post(post_id):
        logger.warning('post %d has been deleted', post_id)
        return redirect(url_for('.posts'))
    else:
        return render_template('page_not_found.html'), 404


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
        return render_template('page_not_found.html'), 404
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
            logger.info('Admin logged in')
            return redirect(url_for('.posts'))
        else:
            logger.warning('Wrong password entered')
            flash('Username or password do not match!')

    return render_template('admin/login.html', form=form)


@blue.route("/logout")
def logout():
    logout_user()
    logger.info('Admin logged out')
    return redirect(url_for('home.index'))


@blue.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_image():
    """Upload a new image to the blog.

    Upload a new image to the website and save the path
    and alt text in the database.
    """
    filename = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No image part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image, created = Image.get_or_create(name=filename)
            if created:
                logger.info('Image %s had been uploaded', filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('The image has been saved.')
            else:
                flash('Filename already exists.')

    return render_template('admin/upload.html')


@blue.route("/imagelist/<int:page_number>")
@login_required
def return_image_list(page_number):
    """Return a HTML page with 15 images of the paginated image model.

    :param page_number: The requested page number
    :return: image_list.html with n amount of images of the requested page number
    """
    number_of_images = 3
    total_image_count = Image.select().count()
    amount_of_pages = total_image_count / number_of_images
    images = Image.select().order_by(Image.id.asc()).paginate(page_number,
                                                              number_of_images)
    return render_template('admin/image_list.html', images=images,
                           amount_of_pages=amount_of_pages)
