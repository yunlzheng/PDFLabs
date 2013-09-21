# -*- coding : utf-8 -*-
import json
import datetime
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado.log import app_log
from handlers import BaseHandler
from models.books import Book

class IWantApi(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, bookid):
        '''
            I want some book
            argument bookid : the book uuid in douban
        '''
        try:
            book = Book.objects(bid=bookid)[0]
            #book.image = book_details['images']['large']
        except Exception, e:
            app_log.error(e)
            http_client = AsyncHTTPClient()
            response = yield http_client.fetch("https://api.douban.com/v2/book/"+bookid)
            book_details = json.loads(response.body)
            book = Book(bid = book_details['id'],
                title=book_details['title'],
                image=book_details['images']['large'],
                isbn13=book_details['isbn13'],
                publisher=book_details['publisher'],
                wcount=0,
                dcount=0
            )
        else:
            book.wcount = book.wcount+1
        finally:
            book.update_at=datetime.datetime.now()
            book.save()

class BookApiHandler(BaseHandler):

    def get(self,id):
        book = Book.objects(bid=id)[0]
        self.write(book.to_json())

class BookDetailHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, id):
        self.set_header('Content-Type', 'application/json')
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://api.douban.com/v2/book/"+id)
        book_details = json.loads(response.body)
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
