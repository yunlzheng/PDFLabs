# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *
from models.users import User
from models.files import File


class Category(Document):
    name = StringField(required=True, unique=True, help_text="Book Category")
    created_at = DateTimeField(default=datetime.datetime.now(), help_text="create datetime")


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
    category = ReferenceField(Category)
    comments = ListField(EmbeddedDocumentField(Comment))
    files = ListField(EmbeddedDocumentField(File))
    wcount = IntField(default=0)
    dcount = IntField()
    # the liked user List
    likes = ListField(ReferenceField(User))
    # the user list who want this book
    wants = ListField()

    meta = {
        'ordering' : ['-update_at']
    }
