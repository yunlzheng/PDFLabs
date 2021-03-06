# -*- coding : utf-8 -*-
import datetime

from tornado.log import app_log
from tornado.web import authenticated

from models.posts import Post
from models.posts import Comment
from handlers import BaseHandler


class PostHandler(BaseHandler):
    def get(self, tag, uuid):
        try:
            post = Post.objects(id=uuid)[0]
            self.render(
                "group/_post.html",
                page_heading=post.title,
                post=post,
                groups=self.get_groups()
            )
        except Exception as ex:
            app_log.error(ex)
            self.redirect('/group/' + tag)


    @authenticated
    def post(self, tag, uuid):
        content = self.get_argument('content')
        now = datetime.datetime.now()
        comment = Comment(content=content,
                          author=self.get_curent_user_model(),
                          create_at=now,
                          update_at=now)
        post = Post.objects(id=uuid)[0]
        post.comments.append(comment)
        post.save()
        self.redirect("/group/" + tag + "/" + uuid)

    @authenticated
    def delete(self, tag, uuid):
        post = Post.objects(id=uuid)[0]
        post.delete()
        self.write('success')

