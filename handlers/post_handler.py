# -*- coding : utf-8 -*-

import tornado.web
from handlers import BaseHandler
from models.bbs import Bbs
from models.post import Post

class PostHandler(BaseHandler):

    def get(self, tag, uuid):
        bbs = Bbs.objects(tag = tag)[0]
        _post = None
        for post in bbs.posts:
            if post.id == uuid:
                _post = post
        self.render(
            "post.html",
            page_heading=bbs.name,
            bbs = bbs,
            post = _post,
            bbss = self.get_bbs()
        )

