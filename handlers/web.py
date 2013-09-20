#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
from tornado.httpclient import *
from handlers import BaseHandler


class LogsHandler(BaseHandler):

    ''' redirect to the update logs page '''

    def get(self):
        self.render(
            "logs.html",
            page_heading='PDFLabs 更新日志',
            groups = self.get_groups()
        )
