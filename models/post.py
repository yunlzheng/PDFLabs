# -*- coding : utf-8 -*-

from mongoengine import *
from mongoengine.fields import *
from models.users import User
from models.post_comments import PostComment

class Post(EmbeddedDocument):
    id =StringField(required=True)
    title = StringField(required=True)
    author = ReferenceField(User)
    content =StringField(required=True)
    comments = ListField(EmbeddedDocumentField(PostComment))
    create_at = DateTimeField()
    update_at = DateTimeField()
