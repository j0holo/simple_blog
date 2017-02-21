from .baseModel import BaseModel
from peewee import *


class Image(BaseModel):
    """The image models for the database.

    post_id - the primary key.
    name - name of the image including the extension.
    """
    name = CharField(max_length=255, unique=True)