# -*- coding : utf-8 -*-

from handlers import BaseHandler
from models.posts import Post

class PostHandler(BaseHandler):

    def get(self, tag, uuid):
        post = Post.objects()[0]
        self.render(
            "post.html",
            page_heading=post.title,
            post = post,
            groups = self.get_groups()
        )

