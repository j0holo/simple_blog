from flask import Flask, request
from datetime import timedelta
from .models import db

app = Flask(__name__)
app.config.from_object('config')
app.permanent_session_lifetime = timedelta(minutes=120)

# removes whitespaces that are created by the template engine
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db.init(app.config['DATABASE'])

from .views import admin, home, post

app.register_blueprint(admin.blue)
app.register_blueprint(home.blue)
app.register_blueprint(post.blue)

