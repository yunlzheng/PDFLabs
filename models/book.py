# -*- coding : utf-8 -*-

from mongoengine import Document
from mongoengine.fields import StringField, ListField, EmailField ,DateTimeField, IntField, UUIDField

class Book(Document):
    id = StringField(required=True)
    title = StringField()
    image = StringField()
    isbn13 = StringField()
    publisher = StringField()
    create_date = DateTimeField()
    want_count = IntField()
    download_count = IntField()
    wishs = ListField(StringField())