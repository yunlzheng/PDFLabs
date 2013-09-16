#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
import tornado.gen
import tornado.httpclient

from tornado.httpclient import *


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")

