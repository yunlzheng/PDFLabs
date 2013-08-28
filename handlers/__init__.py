#!/usr/bin/env python
#*-* coding:utf-8 *-
import time
import os.path
import tornado.web
import tornado.gen
import tornado.httpclient
import motor
import qrcode
from bson.py3compat import b
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import *
from tornado.httpclient import AsyncHTTPClient


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")

