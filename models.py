from peewee import *
import datetime
from flask_login import UserMixin

import os
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ: # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('tea.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Tea(Model):
    name = CharField()
    recipe = CharField()
    brew_time = CharField()
    
    #tags
    has_dairy = BooleanField(default=False)
    has_caffeine = BooleanField(default=False)
    serve_iced = BooleanField(default=False)

    # user is going to become integrated
    creator = ForeignKeyField(User, backref='tea')

    post_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Tea], safe=True)
    print("DB connected & tables created")
    DATABASE.close()