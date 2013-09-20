#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
import tornado.gen
import tornado.httpclient

from tornado.log import app_log
from tornado.httpclient import *

from models.books import Book
from models.groups import Group
from models.users import User
from models.admin import Admin

class UUIDMixin():

    def generate_uuid(self):
        date = datetime.datetime.now()
        return date.strftime("%Y%m%d%Hx%M%S")

class BBSMixin():

    def get_groups(self):
        return Group.objects()

class BaseHandler(tornado.web.RequestHandler, BBSMixin, UUIDMixin):

    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")

    def get_curent_user_model(self):
        uid = self.get_current_user()
        try:
        	user = User.objects(uid=uid)[0]
        except Exception as ex:
        	app_log.error(ex)
        else:
        	return user

class AdminBaseHandler(BaseHandler):

    def get_current_user(self):
        return self.get_secure_cookie("adminid")

    def get_current_admin_model(self):
        admin_id =self.get_current_user()
        try:
            admin = Admin.objects(uuid=admin_id)[0]
        except Exception as ex:
            app_log.error(ex)
        else:
            return admin

class MainHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):

        books = []
        hot_books = Book.objects().order_by('-wcount')[:8]
        for book in Book.objects().order_by('+update_at'):
            books.append(book)

        books.reverse()
        self.render(
            "home.html",
            page_heading='PDFLabs',
            books=books,
            hot_books=hot_books,
            groups = self.get_groups()
        )

