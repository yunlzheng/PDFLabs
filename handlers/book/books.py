# -*- coding : utf-8 -*-
import tornado.web
import tornado.gen

from models.books import Book
from handlers import BaseHandler

class BooksHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        tags = ['shared', 'waiting']
        tag = self.get_arguments('tag')
        books = Book.objects()
        self.render(
            "book/books.html",
            page_heading='test',
            books=books,
            groups = self.get_groups()
        )
