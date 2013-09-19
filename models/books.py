# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *
from models.users import User
from models.files import File

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    author = ReferenceField(User)

class Book(Document):
    bid = StringField(required=True)
    title = StringField(required=True)
    isbn13 = StringField()
    image = StringField()
    publisher = StringField()
    create_at = DateTimeField()
    update_at = DateTimeField()
    comments = ListField(EmbeddedDocumentField(Comment))
    files = ListField(EmbeddedDocumentField(File))
    wcount = IntField(default=0)
    dcount = IntField()

    meta = {
        'ordering' : ['-update_at']
    }
