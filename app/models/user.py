import bcrypt
from .baseModel import BaseModel, db
from peewee import *


class User(BaseModel):
    """The user model for the database.

    Each user can add a post and update every other post, even if those posts
    were created by other users. Users are administrators, not regular users
    who can comment on posts.

    email - the email of the user.
    pw_hash - a Bcrypt hash of the password.
    """
    email = CharField(unique=True, max_length=254)
    pw_hash = CharField()

    @staticmethod
    def add_user(email, password):
        """Add a new user to database.

        :param email: email of the new user.
        :param password: password of the new user.
        :return: True if the user has been created or False if the email
            address is already taken.
        """
        pw_hash = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(14))
        try:
            User.create(email=email, pw_hash=pw_hash)
            return True
        except IntegrityError:
            return False

    @staticmethod
    def check_password(email, password):
        """Check the password entered by the user.

        Currently there is a time difference between a user that does exist and
        one that doesn't. A malicious person could use that as an advantage to
        get a hold of a valid email address. As I'm currently aware, there is no
        difference between a correct and a false password.

        :param email: email of the user
        :param password: password of the user
        :return: True if the hashed password is equal to the hashed password
            stored in the database, else False if it does not match.
        """
        try:
            user = User.get(User.email == email)
            return bcrypt.hashpw(str.encode(password),
                                 str.encode(user.pw_hash)) == str.encode(
                user.pw_hash)
        except User.DoesNotExist:
            return False

    @staticmethod
    def create_user(email, password):
        """Create a new user.

        A user can create, update and delete posts. Currently
        it's not possible to delete posts.

        :param email: the email address the user will be identified with, must be unique.
        :param password: the password of the new user.

        :return: True if user was added successfully, or false if the user already exists.
        """
        db.connect()
        try:
            User.add_user(email, password)
            return True
        except IntegrityError:
            return False
        finally:
            db.close()

    @staticmethod
    def update_user(old_email, new_email=None, password=None):
        """Update the email and password of the user.

        Old_email is required, new_email and password are optional, if both parameters are
        empty update_user() will do nothing. Not asking for the current password is
        intentional, creating and updating are only possible while connected to the server
        via SSH. If a malicious person is on your server you got other problems than just
        protecting your blog account.

        :param old_email: the old email address of the user.
        :param new_email: the new email address of the user.
        :param password: the new password of the user.
        :return: True if the user was updated, even if no parameters where given. Otherwise
            it will return False if the user does not exist.
        """
        db.connect()
        try:
            user = User.get(User.email == old_email)
        except User.DoesNotExist:
            print("The user: {} does not exist".format(old_email))
            return False
        old_hash = user.password
        if new_email:
            user.email = new_email
        if password:
            user.password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(12))
        user.save()
        print("The user has been updated:\n"
              "old email: {}\n"
              "new email: {}\n"
              "password has been updated: {}".format(old_email,
                                                     old_email if new_email is None else new_email,
                                                     old_hash != user.password))
        db.close()
        return True

    @staticmethod
    def delete_user(email):
        """Delete an existing user.

        :param email: email of the user
        :return: True if user could be deleted or False if the user doesn't exist.
        """
        db.connect()
        try:
            user = User.get(User.email == email)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
        finally:
            db.close()
