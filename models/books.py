# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *

from models.book_comments import BookComment
from models.files import File

class Book(Document):
    bid = StringField(required=True)
    title = StringField(required=True)
    isbn13 = StringField()
    image = StringField()
    publisher = StringField()
    create_at = DateTimeField()
    comments = ListField(EmbeddedDocumentField(BookComment))
    files = ListField(EmbeddedDocumentField(File))
    wcount = IntField(default=0)
    dcount = IntField()
