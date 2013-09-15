# -*- coding : utf-8 -*-
import json
import datetime
import tornado.web
import tornado.gen
import motor
from tornado.httpclient import AsyncHTTPClient
from tornado.log import app_log
from . import BaseHandler

class AccountAPI(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, uid):
        self.collection = self.settings['db'].account
        self.set_header('Content-Type', 'application/json')
        account = yield motor.Op(self.collection.find_one, {'uid': uid})
        if account is None:
            self.set_status(404)
            response = {
                'msg': 'account not exist',
                'code': 1001,
                'request': "%s  %s" % (self.request.method, self.request.uri)
            }
            self.write(response)
        else:
            del account['_id']
            if account.get('access_token', None):
                del account['access_token']
            if account.get('refresh_token', None):
                del account['refresh_token']
            self.write(account)

class IWantService(BaseHandler):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, bookid):
        '''  
            I want some book 
            argument bookid : the book uuid in douban
        '''
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://api.douban.com/v2/book/"+bookid)
        book_details = json.loads(response.body)
        uid = self.get_current_user()

        book = {
            'id':book_details['id'],
            'title':book_details['title'],
            'image':book_details['image'],
            'isbn13':book_details['isbn13'],
            'publisher':book_details['publisher'],
            'create_date':datetime.datetime.now(),
            'want_count':0,
            'download_count':0,
            'wishs':[]
        }

        tmp_book = yield motor.Op(self.settings['db'].books.find_one, {'id': book['id']})
        if not tmp_book:
            arguments = yield motor.Op(self.settings['db'].books.insert, book)
            app_log.debug(arguments)
        else:
            _id = tmp_book['_id']
            count = tmp_book['want_count'] +1
            book = yield motor.Op(self.settings['db'].books.update, {'_id':_id},{'$set': {'want_count' : count}})
        print book