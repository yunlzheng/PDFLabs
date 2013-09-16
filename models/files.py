# -*- coding : utf-8 -*-

from mongoengine import *

from models.file_comments import FileComment
from models.users import User

class File(EmbeddedDocument):
   
    file_type = StringField(help_text='the local file or the network disk share')
    file_address = StringField(help_text='the addree to vist the file')
    star = IntField(min_value=0, max_value=5, default=0, help_text='the file star')
    author = ReferenceField(User)
    create_at = DateTimeField(help_text='the time to upload the file')
    comments = ListField(EmbeddedDocumentField(FileComment))


