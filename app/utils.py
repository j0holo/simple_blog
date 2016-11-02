from flask import session, redirect, url_for
from functools import wraps
import markdown

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            # return redirect(url_for('admin.login'))
            pass
        return f(*args, **kwargs)

    return inner

def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id


def logout_user():
    session['logged_in'] = False
    session['user_id'] = None

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
