#!/usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.log import app_log

from models.books import Book
from models.groups import Group
from models.users import User


class BBSMixin():
    def get_groups(self):
        return Group.objects()


class BaseHandler(tornado.web.RequestHandler, BBSMixin):
    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")

    def get_curent_user_model(self):
        id = self.get_current_user()
        try:
            user = User.objects(id=id)[0]
        except Exception as ex:
            app_log.error(ex)
        else:
            return user

    def is_admin(self):
        return self.get_secure_cookie('admin')


class MakoHandler(BaseHandler):
    def initialize(self, lookup):
        self._lookup = lookup

    def render_string(self, filename, **kwargs):
        template = self._lookup.get_template(filename)
        env_kwargs = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.application.reverse_url,
        )
        env_kwargs.update(kwargs)
        return template.render(**env_kwargs)

    def render(self, filename, **kwargs):
        self.finish(self.render_string(filename, **kwargs))


class MainHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        result = {}
        hot_books = Book.objects().order_by('-wcount')[:12]
        query_books = Book.objects().order_by('-update_at')
        rows = int(len(query_books) / 4)
        for row in xrange(rows):
            offset = row * 4
            result[row] = query_books[offset:offset + 4]

        self.render(
            "home.html",
            page_heading='PDFLabs',
            rows=rows,
            hot_books=hot_books,
            groups=self.get_groups(),
            result=result
        )

