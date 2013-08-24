#!/usr/bin/env python
#*-* coding:utf-8 *-

import tornado.web
import motor
from tornado.options import options
from . import BaseHandler

class MainHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):

        books = []
        hot_books = []
        n = yield motor.Op(self.settings['db'].books.find().count)
        if n < 16:
            begin = 0
            end = 16
        else:
            begin = n - 16
            end = n

        cursor = self.settings['db'].books.find().sort('DESCENDING')[begin:end]

        for document in (yield motor.Op(cursor.to_list)):
            books.append(document)

        cursor1 = self.settings['db'].books.find().sort('DESCENDING')
        for document in (yield motor.Op(cursor1.to_list)):
            hot_books.append(document)

        books.reverse()

        self.render(
            "home.html",
            page_heading='PDFLabs',
            books=books,
            hot_books=hot_books
        )


class DevHandler(BaseHandler):

    #@tornado.web.authenticated
    def get(self):
        self.render(
            "dev.html",
            page_heading='PDFLabs|贡献者'
        )


class BookHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        self.collection = self.settings['db'].books
        book = yield motor.Op(self.collection.find_one, {'id': bookid})
        self.render(
            "book.html",
            page_heading=book['title'],
            book=book
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
            page_heading='PDFLabs 更新日志'
        )
