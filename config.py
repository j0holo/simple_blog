class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = 'app/blog.db'
    UPLOAD_FOLDER = 'app/static/images'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "do not use in production"


class ProductionConfig(Config):
    SECRET_KEY = "set this to a secret key in production"
