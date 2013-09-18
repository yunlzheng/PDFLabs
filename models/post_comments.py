# -*- coding : utf-8 -*-

from mongoengine import *
from models.users import User

class PostComment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    author = ReferenceField(User)
    create_at = DateTimeField()
    praise = IntField(default=0)

