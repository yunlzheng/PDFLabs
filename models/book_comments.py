# -*- coding : utf-8 -*-

from mongoengine import *
from models.users import User

class BookComment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    author = ReferenceField(User)
