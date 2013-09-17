# -*- coding : utf-8 -*-
import json
import datetime
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from tornado.log import app_log
from handlers import BaseHandler
from models.users import User 
from models.books import Book

class AccountAPI(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, uid):
        self.set_header('Content-Type', 'application/json')
        try:
            user = User.objects(uid=uid)[0]
        except Exception as ex:
            app_log.error(ex)
            self.set_status(404)
            response = {
                'msg': 'account not exist',
                'code': 1001,
                'request': "%s  %s" % (self.request.method, self.request.uri)
            }
            self.write(response)
        else:
            response={
                'name':user.name,
                'avatar':user.avatar
            }
            self.write(response)

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
        try:
            book = Book.objects(bid=book_details['id'])[0]
            book.image = book_details['images']['large']
        except Exception, e:
            app_log.error(e)
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