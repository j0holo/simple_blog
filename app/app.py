from flask import Flask, render_template, session, flash
from flask import request, Markup, redirect, url_for, abort
from models import Post, User, db
from forms import LoginForm
from functools import wraps
from datetime import datetime, timedelta
import markdown
import html2text

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SERVER_CONFIG', silent=True)
app.permanent_session_lifetime = timedelta(minutes=120)
# removes whitespaces that are created by the template engine
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return inner


@app.before_request
def before_request():
    session.permanent = True;
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route("/")
def home():
    posts = Post.select().order_by(Post.post_date.desc())
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def single_post(post_id):
    post = Post.get(Post.id == post_id)
    return render_template("post.html", post=post)


@app.route("/post/add", methods=['GET', 'POST'])
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

            return render_template("add_post.html",
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
                    return redirect(url_for('home'))
                else:
                    return "The title already exist"
    else:
        return render_template("add_post.html")


@app.route("/post/update/<int:post_id>", methods=['GET', 'POST'])
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
            return render_template("update_post.html",
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
                post.last_edit = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                post.save()
                flash("Post was updated")
                return redirect(url_for('home'))

    title = post.title
    markdown = html2text.html2text(post.text)
    html = filter_markdown(markdown)
    return render_template("update_post.html",
                           title=title,
                           markdown=markdown,
                           html=Markup(html),
                           post_id=post.id)


@app.route("/posts/")
@login_required
def post_overview():
    # TODO: Create an overview of all posts
    posts = Post.select().order_by(Post.post_date.desc())
    return render_template("post_overview.html", posts=posts)


@app.route("/post/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    # TODO: Delete a post
    pass


@app.route("/post/visible/<int:post_id>")
@login_required
def switch_post_visibility(post_id):
    # TODO: Enable function to switch
    """Switch the visible boolean of the post object.

    Read the post.visible field form the post object and
    flip the value to change the visibility.

    :param post_id: id of the post object
    :return: None
    """
    pass


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        if User.check_password(email, password):
            user = User.get(User.email == email)
            auth_user(user)
            flash('You are now logged in')
            return redirect(url_for('home'))
        else:
            flash('Username or password do not match!')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id


def logout_user():
    session['logged_in'] = False
    session['user_id'] = None


def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])


def filter_markdown(markdown_text):
    """Convert the markdown to html.

    Also filters script tags from the html
    """
    html = markdown.markdown(markdown_text)

    while "<script>" in html:
        html = html.replace("<script>", "")
    while "</script>" in html:
        html = html.replace("</script>", "")
    return html


if __name__ == "__main__":
    # db.init(app.config['DATABASE'])
    app.run()
