# -*- coding : utf-8 -*-

from models.posts import Post
from models.groups import Group
from handlers import BaseHandler

class GroupHandler(BaseHandler):

    def get(self, tag):
        group = Group.objects(tag = tag)[0]
        posts = Post.objects(group=group)
        print group.name
        self.render(
            "groups.html",
            page_heading=group.name,
            _group = group,
            posts = posts,
            groups = self.get_groups()
        )
