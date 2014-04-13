# -*- coding : utf-8 -*-
import datetime

from tornado.log import app_log

from models.posts import Post
from models.groups import Group
from handlers import BaseHandler
from decorators import authenticated


class GroupHandler(BaseHandler):
    def get(self, tag):
        group = Group.objects(tag=tag)[0]
        posts = Post.objects(group=group)
        self.render(
            "group/_groups.html",
            page_heading=group.name,
            _group=group,
            posts=posts,
            groups=self.get_groups()
        )

    @authenticated
    def post(self, tag):
        group = Group.objects(tag=tag)[0]
        title = self.get_argument('title')
        content = self.get_argument('content')
        now = datetime.datetime.now()
        mode = self.get_argument('type').decode()
        if mode == 'new':
            try:
                if not title:
                    raise Exception('title is none')
                post = Post(group=group,
                            author=self.get_curent_user_model(),
                            title=title,
                            content=content,
                            create_at=now,
                            update_at=now
                )
                post.save()
                return self.redirect("/group/" + tag + "/" + str(post.id))
            except Exception as ex:
                app_log.error(ex)
                return self.redirect("/group/" + tag)
        elif mode == 'update':
            id = self.get_argument('id')
            try:
                app_log.debug(id)
                app_log.debug(title)
                app_log.debug(content)
                post = Post.objects(id=id)[0]
                post.title = title
                post.content = content
                post.save()
            except Exception as ex:
                app_log.error(ex)
            return self.redirect("/group/" + tag + "/" + id)



