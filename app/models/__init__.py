from peewee import SqliteDatabase

# FIXME: DATABASE const should be set in config.py, setup_server.py still uses a string.
DATABASE = None
db = SqliteDatabase(DATABASE)
