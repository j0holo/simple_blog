from functools import wraps

import markdown
from flask import session, abort

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return abort(404)
        return f(*args, **kwargs)

    return inner


def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id


def logout_user():
    session['logged_in'] = False
    session['user_id'] = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def filter_markdown(markdown_text):
    """Convert the markdown to html.

    And enable markdown extensions.
    """
    #TODO: Enable table extension
    html = markdown.markdown(markdown_text)
    return html
