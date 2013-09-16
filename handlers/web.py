#!/usr/bin/env python
#*-* coding:utf-8 *-
import time
import os.path
import tornado.web
import tornado.gen
import tornado.httpclient
import motor
from tornado.log import app_log
from tornado.httpclient import *

from handlers import BaseHandler


class MainHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):

        books = []
        hot_books = []
        begin = 0
        end = 0
        try:
            n = yield motor.Op(self.settings['db'].books.find().count)
            if n < 16:
                begin = 0
                end = 16
            else:
                begin = n - 16
                end = n
        except Exception as e:
            app_log.error(e)

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

class ContributeHandler(BaseHandler):

    ''' contribute new book resources handler '''
    @tornado.web.authenticated
    def get(self):
        self.render(
            "contribute_book.html",
            page_heading='cuttle | contribute book'
        )

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        db = self.settings['db']
        self.collection = db.books
        id = self.get_argument('id', '')
        title = self.get_argument('title', '')
        image = self.get_argument('image', '')
        isbn13 = self.get_argument('isbn13', '')
        publisher = self.get_argument('publisher', '')
        resource_url = self.get_argument('resource_url', '')

        book = {
            'id': id,
            'title': title,
            'image': image,
            'isbn13': isbn13,
            'publisher': publisher,
            'create_date': time.strftime('%Y-%m-%d %X', time.localtime()),
            'download_count': 0
        }

        if resource_url:
            book['network_disk'] = [resource_url]

        uid = self.get_current_user()
        account = yield motor.Op(self.settings['db'].account.find_one, {'uid': uid})
        # create network disk download link qrcode
        # save file to mingodb gridfs
        try:
            self.request.files['file']
            uploadFile = self.request.files['file'][0]
            filename = uploadFile['filename']
            index = filename.rindex('.')
            fiexed = filename[index:]
            upload_file_path = 'static'
            file_obj = open(upload_file_path + os.path.sep +
                            'doc' + os.path.sep + id + fiexed, 'w+')
            file_obj.write(uploadFile['body'])
            # save the file to mongo gridfs
            # f = yield motor.Op(motor.MotorGridIn(db.fs, filename=filename).open)
            # yield motor.Op(f.write, file_obj)
            # yield motor.Op(f.close)
            book_file = {
                'account': account,
                'file': id + fiexed
            }
            book['files'] = [book_file]
        except:
            pass

        # create qrcode images

        # root = self.settings['root']
        # qrcode_content = ''
        # if resource_url:
        #     qrcode_content += resource_url
        # elif book['files']:
        #     qrcode_content = self.settings[
        #         'root'] + "static/doc/" + book["title"]

        # img = qrcode.make(qrcode_content)
        # img.save('static/qrcode/' + book_id + ".png")

        document = yield motor.Op(self.collection.find_one, {'id': id})
        if document is None:
            arguments = yield motor.Op(self.collection.insert, book)
            app_log.info('contribute a new book resources')
        else:
            app_log.debug('book info alredy exist...')
            pass
        self.redirect("/book/" + id)