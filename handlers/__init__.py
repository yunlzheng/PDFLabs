#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
import tornado.gen
import tornado.httpclient

from tornado.log import app_log
from tornado.httpclient import *
from models.users import User

class BaseHandler(tornado.web.RequestHandler):

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

