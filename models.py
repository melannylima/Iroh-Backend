from peewee import *
import datetime

DATABASE = SqliteDatabase('tea.sqlite')

class Tea(Model):
    name = CharField()
    recipe = CharField()
    brew_time = CharField()
    
    #tags
    has_dairy = BooleanField(default=False)
    has_caffeine = BooleanField(default=False)
    serve_iced = BooleanField(default=False)

    # user is going to become integrated
    creator = CharField()

    post_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Tea], safe=True)
    print("DB connected")
    DATABASE.close()