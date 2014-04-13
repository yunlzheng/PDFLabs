# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *


class Group(Document):
    name = StringField(required=True)
    tag = StringField(required=True)
    description = StringField(required=True)
    create_at = DateTimeField()
    update_at = DateTimeField()
