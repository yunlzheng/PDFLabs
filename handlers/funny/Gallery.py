# coding: utf-8
from handlers import BaseHandler
from models.users import User


class UserGalleryHandler(BaseHandler):
    def get(self):
        self.render("funny/gallery.html", page_heading="画廊", groups=self.get_groups());


class UserGalleryApiHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        users = User.objects() \
            .exclude("password").exclude("access_token").exclude("uid").exclude('password')
        self.write(users.to_json())