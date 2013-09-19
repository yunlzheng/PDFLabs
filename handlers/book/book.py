# -*- coding : utf-8 -*-
import datetime

import tornado.web
import tornado.gen
from tornado.log import app_log

from models.books import Book
from models.files import File
from handlers import BaseHandler

class BookHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        book = Book.objects(bid = bookid)[0]
        self.render(
            "book/book.html",
            page_heading=book.title,
            book=book,
            groups = self.get_groups()
        )

    @tornado.web.authenticated
    def post(self, bookid):
        resource_url = self.get_argument('resource_url', None)
        if resource_url:
            try:
                book = Book.objects(bid=bookid)[0]
            except Exception as ex:
                app_log.error(ex)
            else:
                user = self.get_curent_user_model()
                file = File(file_type='network_disk',
                        file_address=resource_url,
                )
                file.author = user
                book.files.append(file)
                book.update_at=datetime.datetime.now()
                book.save()
        self.redirect("/book/" + bookid)


class PreviewHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        book = Book.objects(bid = bookid)[0]
        self.render(
            "preview.html",
            page_heading=book['title'],
            book=book,
            groups = self.get_groups()
        )
