# -*- coding : utf-8 -*-
import tornado.web
import tornado.gen
from tornado.log import app_log
from models.users import User

class UserAPI(tornado.web.RequestHandler):

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
            self.write(user.to_json())

