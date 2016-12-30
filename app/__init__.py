import logging
from datetime import timedelta

from flask import Flask

from .models import db

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
app.permanent_session_lifetime = timedelta(minutes=120)

# This isn't the prettiest option to dissable the werkzeug logger
# but it works and stops polluting my own log. If I could
# seperate my log from werkzeug that would be great.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# removes whitespaces that are created by the template engine
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db.init(app.config['DATABASE'])

from .views import admin, home, post

app.register_blueprint(admin.blue)
app.register_blueprint(home.blue)
app.register_blueprint(post.blue)
