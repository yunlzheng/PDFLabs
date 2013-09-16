#!/usr/bin/env python
#*-* coding:utf-8 *-
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
        for book in Book.objects():
            books.append(book)

        self.render(
            "home.html",
            page_heading='PDFLabs',
            books=books,
            hot_books=books[-8:]
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
        book = Book.objects(bid = bookid)[0]
        self.render(
            "book.html",
            page_heading=book.title,
            book=book
        )

class PreviewHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, bookid):
        self.collection = self.settings['db'].books
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
            print ">++++++++++++++++++++++++++++++"
            book.files.append(file)
            book.save()
        except Exception as ex:
            app_log.error(ex)
        self.redirect("/book/" + str(book.bid))

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):

        id = self.get_argument('id', '')
        title = self.get_argument('title', '')
        image = self.get_argument('image', '')
        isbn13 = self.get_argument('isbn13', '')
        publisher = self.get_argument('publisher', '')
        resource_url = self.get_argument('resource_url', '')

        try: 
            book = Book.objects(bid=id)[0]
        except Exception as ex:
            app_log.error(ex)
            book = Book(bid = id, 
                title=title, 
                image=image, 
                isbn13=isbn13,
                publisher=publisher,
                wcount=0,
                dcount=0
            )
        finally:
            book.save()

        if resource_url:
            self.share_network_file(book, resource_url)
        else:
            self.share_local_file(book, resource_url)