# -*- coding : utf-8 -*-

from mongoengine import *

class User(Document):
    uid = StringField(required=True)
    type = StringField(required=True)
    email = StringField(required=True)
    name = StringField(max_length=50)
    avatar = URLField()
    access_token = StringField()
    refresh_token = StringField()