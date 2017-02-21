from app.seeder import posts
from .image import Image
from .post import Post
from .user import User
from . import db
import time


# Helper functions
def create_tables():
    """Creates new tables, drop the current tables.

    :return: True if tables where created successfully, otherwise False.
    """
    db.drop_tables([Post, User, Image], safe=True)
    db.create_tables([Post, User, Image])
    if User.table_exists() and Post.table_exists():
        return True
    else:
        return False


def populate_tables():
    """Fill database tables with demo data.

     This function is used for testing only. The random text from seeder.py
     was generated with http://randomtextgenerator.com/
    """
    db.connect()
    User.add_user("invalid@invalid.com", "devpassword")
    Post.add_post(posts[0]['title'], posts[0]['text'])
    Post.add_post(posts[1]['title'], posts[1]['text'])
    db.close()
