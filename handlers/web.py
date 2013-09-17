#!/usr/bin/env python
#*-* coding:utf-8 *-
import json
import datetime
import os.path
import tornado.web
import tornado.gen
import tornado.httpclient
import motor
from tornado.log import app_log
from tornado.httpclient import *
from models.books import Book
from models.files import File

from handlers import BaseHandler

class UUIDMixin():

    def generate_uuid(self):

        date = datetime.datetime.now()
        return date.strftime("%Y%m%d%Hx%M%S")

class MainHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        
        books = []
        hot_books = Book.objects().order_by('-wcount')[:8]
        for book in Book.objects().order_by('+update_at'):
            books.append(book)

        books.reverse()
        self.render(
            "home.html",
            page_heading='PDFLabs',
            books=books,
            hot_books=hot_books
        )

class BookHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        book = Book.objects(bid = bookid)[0]
        self.render(
            "book.html",
            page_heading=book.title,
            book=book
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
        book = yield motor.Op(self.collection.find_one, {'id': bookid})
        self.render(
            "preview.html",
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

class ContributeHandler(BaseHandler, UUIDMixin):

    ''' contribute new book resources handler '''
    @tornado.web.authenticated
    def get(self):
        self.render(
            "contribute_book.html",
            page_heading='cuttle | contribute book'
        )

    def share_network_file(self, book, resource_url):
        user = self.get_curent_user_model()
        file = File(file_type='network_disk',
                file_address=resource_url,
        )
        if user:
            file.author = user
        book.files.append(file)
        book.update_at=datetime.datetime.now()
        book.save()
        self.redirect("/book/" + book.bid)

    def share_local_file(self,book, resource_url):
        
        user = self.get_curent_user_model()
        try:
            self.request.files['file']
            uploadFile = self.request.files['file'][0]
            filename = uploadFile['filename']
            fiexed = filename[filename.rindex('.'):]
            path = 'static' + os.path.sep +'doc' + os.path.sep + self.generate_uuid() + fiexed
            file_obj = open(path, 'w+')
            file_obj.write(uploadFile['body'])
            file = File(
                file_type='local_disk',
                file_address=path,
            )
            if user:
                file.author = user
            book.files.append(file)
            book.update_at=datetime.datetime.now()
            book.save()
        except Exception as ex:
            app_log.error(ex)
        self.redirect("/book/" + str(book.bid))

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):

        id = self.get_argument('id', '')
        resource_url = self.get_argument('resource_url', '')

        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://api.douban.com/v2/book/"+id)
        response = json.loads(response.body)

        book=None
        try: 
            book = Book.objects(bid=id)[0]
        except Exception as ex:
            app_log.error(ex)
            book = Book(bid = id, 
                title=response['title'], 
                image=response['images']['large'], 
                isbn13=response['isbn13'],
                publisher=response['publisher'],
                wcount=0,
                dcount=0
            )
        finally:
            book.save()

        if resource_url:
            self.share_network_file(book, resource_url)
        else:
            self.share_local_file(book, resource_url)