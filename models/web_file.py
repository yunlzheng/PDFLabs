# -*- coding : utf-8 -*-

from mongoengine import Document
from mongoengine.fields import StringField, ListField, EmailField ,DateTimeField, IntField, URLField, UUIDField

class WebFile(Document):
    id = StringField(required=True)
    uploader = UUIDField()
    upload_date = DateTimeField()
    link_url = URLField()
    start = IntField()