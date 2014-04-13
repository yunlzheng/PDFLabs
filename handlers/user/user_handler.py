# coding: utf-8
from itertools import izip

from handlers import BaseHandler
from models.users import User
from models.books import Book


class UserHandler(BaseHandler):
    def get(self, id):
        user = User.objects(id=id)[0]
        books = Book.objects(likes__in=[user])
        bgs = self.grouped(books)

        kwargs = {
            "page_heading": unicode(user.name),
            "groups": self.get_groups(),
            "user": user,
            "books": books,
            "bgs": bgs
        }
        self.render('user.html', **kwargs)

    def grouped(self, iterable):
        a = iter(iterable)
        return izip(a, a)