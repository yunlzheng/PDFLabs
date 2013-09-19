# -*- coding : utf-8 -*-
import datetime

import tornado.web
from tornado.log import app_log

from models.posts import Post
from models.groups import Group
from handlers import BaseHandler


class PostHandler(BaseHandler):

    def get(self, tag, uuid):
        post = Post.objects(id=uuid)[0]
        self.render(
            "post.html",
            page_heading=post.title,
            post = post,
            groups = self.get_groups()
        )

    @tornado.web.authenticated
    def post(self,tag,uuid):
        group = Group.objects(tag = tag)[0]
        title = self.get_argument('title')
        content = self.get_argument('content')
        now = datetime.datetime.now()
        post = Post(group=group,
            author = self.get_curent_user_model(),
            title=title,
            content=content,
            create_at=now,
            update_at=now
        )
        try:
            post.save()
        except Exception as ex:
            app_log.error(ex)
        self.redirect("/group/"+tag)

