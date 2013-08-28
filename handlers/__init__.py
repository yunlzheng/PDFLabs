#!/usr/bin/env python
#*-* coding:utf-8 *-
import time
import os.path
import tornado.web
import tornado.gen
import tornado.httpclient
import motor
import qrcode
from bson.py3compat import b
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import *
from tornado.httpclient import AsyncHTTPClient


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        # return 1
        return self.get_secure_cookie("userid")


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


class DoubanSearchHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, keyword):
        self.set_header('contentType', 'application/json')
        fields = self.get_argument('fields')
        http_client = AsyncHTTPClient()
        url = "https://api.douban.com/v2/book/search?q=" + \
            keyword + "&fields=" + fields
        response = yield http_client.fetch(url)
        self.write(response.body)
