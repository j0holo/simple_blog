"""Contains database models and helper functions."""
from peewee import *
from app.models import db


class BaseModel(Model):
    """BaseModel class with the database connection object."""

    class Meta:
        database = db
