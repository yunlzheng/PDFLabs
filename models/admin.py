# -*- coding : utf-8 -*-

from mongoengine import *

class Admin(Document):
    uuid = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
