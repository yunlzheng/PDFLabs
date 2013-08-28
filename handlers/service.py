# -*- coding : utf-8 -*-
import json
import tornado.web
import tornado.gen
import motor
from tornado.httpclient import AsyncHTTPClient

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
