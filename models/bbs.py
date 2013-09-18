# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *
from models.post import Post

class Bbs(Document):
    name = StringField(required=True)
    tag = StringField(required=True)
    description = StringField(required=True)
    posts = ListField(EmbeddedDocumentField(Post))
    create_at = DateTimeField()
    update_at = DateTimeField()
