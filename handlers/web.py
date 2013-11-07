#!/usr/bin/env python
#*-* coding:utf-8 *-
import tornado.web
from tornado.httpclient import *
from handlers import BaseHandler
from decorators import log_exception
from decorators import authenticated


class AdminHandler(BaseHandler):
	
	@authenticated	
	def get(self):
		if self.is_admin():
			self.render('admin/admin.html', page_heading='Admin')
		else:
			self.redirect("/")


class LogsHandler(BaseHandler):

    ''' redirect to the update logs page '''
    @log_exception
    def get(self):
        self.render(
            "logs.html",
            page_heading='PDFLabs 更新日志',
            groups=self.get_groups()
        )
