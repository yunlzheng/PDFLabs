#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.httpclient import *
from handlers import BaseHandler

class PreviewHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        book = yield motor.Op(self.collection.find_one, {'id': bookid})
        self.render(
            "preview.html",
            page_heading=book['title'],
            book=book,
            groups = self.get_groups()
        )

class AuthenticateHandler(BaseHandler):

    ''' redirect to the login page '''

    def get(self):
        self.render(
            "sigin.html",
            page_heading='PDFLabs 登录'
        )


class LogsHandler(BaseHandler):

    ''' redirect to the update logs page '''

    def get(self):
        self.render(
            "logs.html",
            page_heading='PDFLabs 更新日志',
            groups = self.get_groups()
        )
