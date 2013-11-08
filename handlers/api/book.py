# -*- coding : utf-8 -*-
import json
import datetime
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado.log import app_log
from handlers import BaseHandler
from models.books import Book
from models.books import Category
from decorators import authenticated


class IWantApi(BaseHandler):

    def get(self, id):
        self.redirect("/book/"+id)

    @authenticated
    def post(self, bookid):

        image = self.get_argument('images[large]')
        title = self.get_argument('title')
        isbn13 = self.get_argument('isbn13')
        bid = self.get_argument('id')
        publisher = self.get_argument('publisher')

        try:
            book = Book.objects(bid=bookid)[0]
        except Exception, e:
            app_log.error(e)
            category = Category.objects(default=True).first()
            book = Book(bid=bid, title=title, image=image, isbn13=isbn13,
                        publisher=publisher, wcount=0, dcount=0, category=category)
        else:
            book.wcount = book.wcount+1
        finally:
            book.update_at = datetime.datetime.now()
            book.save()


class LikeApiHandler(BaseHandler):

    def get(self, id):
        self.redirect("/book/"+id)

    @authenticated
    def post(self, id):
        book = Book.objects(bid=id)[0]
        user = self.get_curent_user_model()
        if user not in book.likes:
            book.likes.append(user)
        else:
            book.likes.remove(user)
        book.save()


class BookDetailHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, id):
        self.set_header('Content-Type', 'application/json')
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://api.douban.com/v2/book/"+id)
        book = Book.objects(bid=id).first()

        book_details = json.loads(response.body)
        book.image = book_details.get('image')
        book.save()
        self.write(book_details)


class BookSearchHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, keyword):
        self.set_header('contentType', 'application/json')
        fields = self.get_argument('fields')
        http_client = AsyncHTTPClient()
        url = "https://api.douban.com/v2/book/search?q=" + \
            keyword + "&fields=" + fields
        response = yield http_client.fetch(url)
        self.write(response.body)
