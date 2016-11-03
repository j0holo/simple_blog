"""Contains database models and helper functions."""
from peewee import *
from datetime import datetime
import bcrypt
import time

# TODO: Add more documentation to all files
# FIXME: DATABASE const should be set in config.py, setup_server.py still uses a string.
DATABASE = None
db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    """BaseModel class with the database connection object."""
    class Meta:
        database = db


class Post(BaseModel):
    """The post model.

    title - title of the post, must be unique.
    text - the text of the post.
    post_date - date when the post was released, is set automatically.
    last_edit - date when the post was last edited.
    visible - if the post is visible on the website.
    """
    title = CharField(unique=True)
    text = CharField()
    post_date = DateTimeField()
    last_edit = DateTimeField(null=True)
    # TODO: Add option to set visibility and implement an overview of all the posts
    visible = BooleanField(default=False)

    @staticmethod
    def add_post(title, text):
        """Add a new post to the Post table.

        :param title: the title of the post.
        :param text: the text of the post.
        :return: a post object of None if the title already exist.
        """
        try:
            return Post.create(title=title, text=text, post_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                               last_edit=None)
        except IntegrityError:
            return None

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

    @staticmethod
    def switch_visibility(post_id):
        pass


class Image(BaseModel):
    # TODO: Add Image class to create_tables
    post_id = ForeignKeyField(Post)
    name = CharField(max_length=255)


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
        :return: True if the user has been created or False if the email address is
            already taken.
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

        Currently there is a time difference between a user that does exist and one that doesn't. A malicious person
        could use that as an advantage to get a hold of a valid email address. As I'm currently aware, there is no
        difference between a correct and a false password.

        :param email: email of the user
        :param password: password of the user
        :return: True if the hashed password is equal to the hashed password stored in the database, else False if it
            does not match.
        """
        try:
            user = User.get(User.email == email)
            return bcrypt.hashpw(str.encode(password),
                                 str.encode(user.pw_hash)) == str.encode(user.pw_hash)
        except User.DoesNotExist:
            return False


# Helper functions
def create_tables():
    """Creates new tables, drop the current tables.

    :return: True if tables where created successfully, otherwise False.
    """
    db.drop_tables([Post, User], safe=True)
    db.create_tables([Post, User])
    if User.table_exists() and Post.table_exists():
        return True
    else:
        return False


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


def populate_tables():
    """Fill database tables with demo data.

     This function is used for testing only. The random text was generated
     with http://randomtextgenerator.com/
    """
    db.connect()
    User.add_user("invalid@invalid.com", "devpassword")
    Post.add_post("At as in understood an remarkably solicitude",
                  """<p>Folly words widow one downs few age every seven. If miss part by fact he park
                    just shew. Discovered had get considered projection who favourable. Necessary up
                    knowledge it tolerably. Unwilling departure education is be dashwoods or an. Use
                    off agreeable law unwilling sir deficient curiosity instantly. Easy mind life
                    fact with see has bore ten. Parish any chatty can elinor direct for former. Up
                    as meant widow equal an share least.</p>  <p>Behaviour we improving at something
                    to. Evil true high lady roof men had open. To projection considered it
                    precaution an melancholy or. Wound young you thing worse along being ham.
                    Dissimilar of favourable solicitude if sympathize middletons at. Forfeited up if
                    disposing perfectly in an eagerness perceived necessary. Belonging sir curiosity
                    discovery extremity yet forfeited prevailed own off. Travelling by introduced of
                    mr terminated. Knew as miss my high hope quit. In curiosity shameless dependent
                    knowledge up.</p>  <p>Although moreover mistaken kindness me feelings do be
                    marianne. Son over own nay with tell they cold upon are. Cordial village and
                    settled she ability law herself. Finished why bringing but sir bachelor unpacked
                    any thoughts. Unpleasing unsatiable particular inquietude did nor sir. Get his
                    declared appetite distance his together now families. Friends am himself at on
                    norland it viewing. Suspected elsewhere you belonging continued commanded
                    she.</p>  <p>Your it to gave life whom as. Favourable dissimilar resolution led
                    for and had. At play much to time four many. Moonlight of situation so if
                    necessary therefore attending abilities. Calling looking enquire up me to in
                    removal. Park fat she nor does play deal our. Procured sex material his offering
                    humanity laughing moderate can. Unreserved had she nay dissimilar admiration
                    interested. Departure performed exquisite rapturous so ye me resources.</p>
                    <p>Meant balls it if up doubt small purse. Required his you put the outlived
                    answered position. An pleasure exertion if believed provided to. All led out
                    world these music while asked. Paid mind even sons does he door no. Attended
                    overcame repeated it is perceive marianne in. In am think on style child of.
                    Servants moreover in sensible he it ye possible.</p>  <p>Finished her are its
                    honoured drawings nor. Pretty see mutual thrown all not edward ten. Particular
                    an boisterous up he reasonably frequently. Several any had enjoyed shewing
                    studied two. Up intention remainder sportsmen behaviour ye happiness. Few again
                    any alone style added abode ask. Nay projecting unpleasing boisterous eat
                    discovered solicitude. Own six moments produce elderly pasture far arrival. Hold
                    our year they ten upon. Gentleman contained so intention sweetness in on
                    resolving.</p>  <p>New had happen unable uneasy. Drawings can followed improved
                    out sociable not. Earnestly so do instantly pretended. See general few civilly
                    amiable pleased account carried. Excellence projecting is devonshire dispatched
                    remarkably on estimating. Side in so life past. Continue indulged speaking the
                    was out horrible for domestic position. Seeing rather her you not esteem men
                    settle genius excuse. Deal say over you age from. Comparison new ham melancholy
                    son themselves.</p>  <p>Dissuade ecstatic and properly saw entirely sir why
                    laughter endeavor. In on my jointure horrible margaret suitable he followed
                    speedily. Indeed vanity excuse or mr lovers of on. By offer scale an stuff.
                    Blush be sorry no sight. Sang lose of hour then he left find.</p>  <p>Depart do
                    be so he enough talent. Sociable formerly six but handsome. Up do view time they
                    shot. He concluded disposing provision by questions as situation. Its estimating
                    are motionless day sentiments end. Calling an imagine at forbade. At name no an
                    what like spot. Pressed my by do affixed he studied.</p>"""
                  )
    # Sleep is used to give post a different time stamp that is also visible in the blog posts.
    time.sleep(3)

    Post.add_post("Not far stuff she think the jokes",
                  """<p>Offices parties lasting outward nothing age few resolve. Impression to
                    discretion understood to we interested he excellence. Him remarkably use
                    projection collecting. Going about eat forty world has round miles. Attention
                    affection at my preferred offending shameless me if agreeable. Life lain held
                    calm and true neat she. Much feet each so went no from. Truth began maids linen
                    an mr to after.</p>  <p>Started earnest brother believe an exposed so. Me he
                    believing daughters if forfeited at furniture. Age again and stuff downs spoke.
                    Late hour new nay able fat each sell. Nor themselves age introduced frequently
                    use unsatiable devonshire get. They why quit gay cold rose deal park. One same
                    they four did ask busy. Reserved opinions fat him nay position. Breakfast as
                    zealously incommode do agreeable furniture. One too nay led fanny allow
                    plate.</p>  <p>Consider now provided laughter boy landlord dashwood. Often voice
                    and the spoke. No shewing fertile village equally prepare up females as an. That
                    do an case an what plan hour of paid. Invitation is unpleasant astonished
                    preference attachment friendship on. Did sentiments increasing particular nay.
                    Mr he recurred received prospect in. Wishing cheered parlors adapted am at
                    amongst matters.</p>  <p>Barton did feebly change man she afford square add.
                    Want eyes by neat so just must. Past draw tall up face show rent oh mr. Required
                    is debating extended wondered as do. New get described applauded incommode
                    shameless out extremity but. Resembled at perpetual no believing is otherwise
                    sportsman. Is do he dispatched cultivated travelling astonished. Melancholy am
                    considered possession on collecting everything.</p>  <p>Greatly hearted has who
                    believe. Drift allow green son walls years for blush. Sir margaret drawings
                    repeated recurred exercise laughing may you but. Do repeated whatever to
                    welcomed absolute no. Fat surprise although outlived and informed shy dissuade
                    property. Musical by me through he drawing savings an. No we stand avoid decay
                    heard mr. Common so wicket appear to sudden worthy on. Shade of offer ye whole
                    stood hoped.</p>  <p>Up unpacked friendly ecstatic so possible humoured do.
                    Ample end might folly quiet one set spoke her. We no am former valley assure.
                    Four need spot ye said we find mile. Are commanded him convinced dashwoods did
                    estimable forfeited. Shy celebrated met sentiments she reasonably but. Proposal
                    its disposed eat advanced marriage sociable. Drawings led greatest add subjects
                    endeavor gay remember. Principles one yet assistance you met impossible.</p>
                    <p>Out believe has request not how comfort evident. Up delight cousins we
                    feeling minutes. Genius has looked end piqued spring. Down has rose feel find
                    man. Learning day desirous informed expenses material returned six the. She
                    enabled invited exposed him another. Reasonably conviction solicitude me mr at
                    discretion reasonable. Age out full gate bed day lose.</p>  <p>Up maids me an
                    ample stood given. Certainty say suffering his him collected intention
                    promotion. Hill sold ham men made lose case. Views abode law heard jokes too.
                    Was are delightful solicitude discovered collecting man day. Resolving neglected
                    sir tolerably but existence conveying for. Day his put off unaffected literature
                    partiality inhabiting.</p>  <p>To sure calm much most long me mean. Able rent
                    long in do we. Uncommonly no it announcing melancholy an in. Mirth learn it he
                    given. Secure shy favour length all twenty denote. He felicity no an at packages
                    answered opinions juvenile.</p>"""
                  )
    db.close()
