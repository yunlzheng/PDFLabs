# -*- coding : utf-8 -*-

from mongoengine import Document
from mongoengine.fields import StringField, ListField, EmailField ,DateTimeField, IntField, 

class LocaleFile(Document):
    id = StringField(required=True)
    uploader = UUIDField()
    upload_date = DateTimeField()
    file_path = StringField()
    start = IntField()