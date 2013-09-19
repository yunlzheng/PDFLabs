#*-* coding:utf-8 *-
import json
import datetime
import os.path
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.log import app_log
from tornado.httpclient import *
from models.books import Book
from models.files import File
from handlers import BaseHandler


class FindHandler(BaseHandler):

    ''' contribute new book resources handler '''
    @tornado.web.authenticated
    def get(self):
        self.render(
            "book/find.html",
            page_heading='cuttle | contribute book',
            groups = self.get_groups()
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
