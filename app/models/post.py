from datetime import datetime

from .baseModel import BaseModel
from peewee import *
from slugify import slugify


class Post(BaseModel):
    """The post model.

    title - title of the post, must be unique.
    text - the text of the post.
    post_date - date when the post was released, is set automatically.
    last_edit - date when the post was last edited.
    visible - if the post is visible on the website.
    """
    title = CharField(unique=True)
    slug = CharField()
    text = CharField()
    post_date = DateField()
    visible = BooleanField(default=False)

    @staticmethod
    def add_post(title, text):
        """Add a new post to the Post table.

        :param title: the title of the post.
        :param text: the text of the post.
        :return: a post object of None if the title already exist.
        """
        try:
            return Post.create(title=title,
                               slug=slugify(title),
                               text=text,
                               post_date=datetime.now().strftime('%Y-%m-%d'))
        except IntegrityError:
            return None

    @staticmethod
    def update_post_date(post_id):
        """Update the time of the post.

        Usefull when you are not finished with your post
        and want to update the time when you make the post
        visible.

        :param post_id:
        :return: True is the post does exist.
        """
        try:
            post = Post.get(Post.id == post_id)
            post.post_date = datetime.now().strftime('%Y-%m-%d')
            post.save()
            return True
        except Post.DoesNotExist:
            return False

    @staticmethod
    def delete_post(post_id):
        """Delete an existing post.

        :param post_id: id of the post.
        :return: True if successful or False if the post doesn't exist.
        """
        try:
            post = Post.get(Post.id == post_id)
            post.delete()
            return True
        except Post.DoesNotExist:
            return False