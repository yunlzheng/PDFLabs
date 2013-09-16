# -*- coding : utf-8 -*-
import json
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient

from . import BaseHandler

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
