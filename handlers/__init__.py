#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
import tornado.gen
import tornado.httpclient

from tornado.log import app_log
from tornado.httpclient import *
from models.bbs import Bbs
from models.users import User
from models.admin import Admin

class UUIDMixin():

    def generate_uuid(self):
        date = datetime.datetime.now()
        return date.strftime("%Y%m%d%Hx%M%S")

class BBSMixin():

    def get_bbs(self):
        return Bbs.objects()

class BaseHandler(tornado.web.RequestHandler, BBSMixin, UUIDMixin):

    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")

    def get_curent_user_model(self):
        uid = self.get_current_user()
        try:
        	user = User.objects(uid=uid)[0]
        except Except as ex:
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
        except Except as ex:
            app_log.error(ex)
        else:
            return admin

