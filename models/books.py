# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *

from models.book_comments import BookComment

class Book(Document):
    title = StringField(required=True)
    isbn13 = StringField()
    publisher = StringField()
    comments = ListField(EmbeddedDocumentField(BookComment))
    wcount = IntField(default=0)
    dcount = IntField()
