# coding: utf-8
import tornado.web
from handlers import BaseHandler
from models.users import User

class UserHandler(BaseHandler):

    def get(self, id):
        user = User.objects(id=id)[0]
        self.render('user.html', page_heading = unicode(user.name), groups = self.get_groups(), user=user)