# -*- coding : utf-8 -*-
import tornado.web
import tornado.gen

from models.books import Book
from handlers import BaseHandler


class BooksHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        tag = self.get_arguments('tag')[0].decode()
        books = Book.objects()
        if tag=='shared':
            books = [book for book in books if book.files]
        elif tag=='waiting':
            books = [book for book in books if not book.files]
        elif tag== 'hot':
            books = Book.objects().order_by('-wcount')[:20]

        self.render(
            "book/books.html",
            page_heading=tag,
            books=books,
            groups=self.get_groups()
        )
