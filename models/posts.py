# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *
from models.users import User
from models.groups import Group

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    author = ReferenceField(User)
    create_at = DateTimeField()
    praise = IntField(default=0)

class Post(Document):
    group = ReferenceField(Group)
    title = StringField(required=True)
    author = ReferenceField(User)
    content =StringField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    create_at = DateTimeField()
    update_at = DateTimeField()

