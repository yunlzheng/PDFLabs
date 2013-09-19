# -*- coding : utf-8 -*-
import tornado.web
import tornado.gen

from models.books import Book
from handlers import BaseHandler

class BooksHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, type):
        books = Book.objects()
        self.render(
            "book/books.html",
            page_heading=type,
            books=books,
            groups = self.get_groups()
        )
