# -*- coding : utf-8 -*-
import datetime

import tornado.web
from tornado.log import app_log

from models.posts import Post
from models.groups import Group
from handlers import BaseHandler

class GroupHandler(BaseHandler):

    def get(self, tag):
        group = Group.objects(tag = tag)[0]
        posts = Post.objects(group=group)
        self.render(
            "groups.html",
            page_heading=group.name,
            _group = group,
            posts = posts,
            groups = self.get_groups()
        )

    @tornado.web.authenticated
    def post(self,tag):
        group = Group.objects(tag = tag)[0]
        title = self.get_argument('title')
        content = self.get_argument('content')
        now = datetime.datetime.now()

        try:
            if not title:
                raise Exception('title is none')
            post = Post(group=group,
                author = self.get_curent_user_model(),
                title=title,
                content=content,
                create_at=now,
                update_at=now
            )
            post.save()
        except Exception as ex:
            app_log.error(ex)
        self.redirect("/group/"+tag)
