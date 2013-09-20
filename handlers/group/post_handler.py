# -*- coding : utf-8 -*-
import datetime

import tornado.web
from tornado.log import app_log

from models.posts import Post
from models.posts import Comment
from models.groups import Group
from handlers import BaseHandler


class PostHandler(BaseHandler):

    def get(self, tag, uuid):
        post = Post.objects(id=uuid)[0]
        self.render(
            "group/post.html",
            page_heading=post.title,
            post = post,
            groups = self.get_groups()
        )

    @tornado.web.authenticated
    def post(self,tag,uuid):
        content = self.get_argument('content')
        now = datetime.datetime.now()
        comment = Comment(content=content,
            author=self.get_curent_user_model(),
            create_at=now,
            update_at=now)
        post = Post.objects(id=uuid)[0]
        post.comments.append(comment)
        post.save()
        self.redirect("/group/"+tag+"/"+uuid)

