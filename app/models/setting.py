from .baseModel import BaseModel
from peewee import *


class Setting(BaseModel):
    """Setting provides multiple settings for more flexibility.

    Settings are stored in a key-value table, currently the following settings
    are present:

    About page text:    Contains the about page text.
    Head Title:         Contains the head title (the text you see in the tab of
        a webbrowser).
    Header page title:  Contains the title/slogan of the website.
    Header logo:        Contains the path to the logo of the website.

    key - key of the row.
    value - value of the row.
    """
    key = CharField(unique=True)
    value = CharField()
    ALLOWED_KEYS = ['about_text', 'head_title', 'header_title', 'header_logo']

    @staticmethod
    def set_value(key, value):
        """Insert or update a value of a specific key.

        Only keys that match ALLOWED_KEYS are able to be inserted or updated.
        If a key does not exist, the function will create a new Setting object
        with the specified key, otherwise it will update the existing key.
        Only the value is allowed to be updated.

        :param key: The key that must be inserted or updated.
        :param value: The value that belongs to the specified key.
        :return: True if value is update, False if key does not match
            ALLOWED_KEYS or integrity_error.
        """
        pass
