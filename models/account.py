# -*- coding : utf-8 -*-

from mongoengine import Document
from mongoengine.fields import StringField, ListField, EmailField, UUIDField

class Account(Document):
    id = UUIDField(required=True)
    name = StringField(required=True)
    avator = StringField(required=True)
    email = EmailField(required=True)
    platform = StringField(required=True)
