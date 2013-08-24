#!/usr/bin/env python
#*-* coding:utf-8 *-

#	Sample main.py Tornado file
#
#	Author: Zheng yunlong
#
import os
import os.path
import time
import datetime
import json
import urllib
import urllib2
import unicodedata

import motor
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.auth
from tornado.log import app_log
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options

from handlers import BaseHandler, ContributeHandler, DoubanSearchHandler
from handlers.weixin import WeiXinHandler
from handlers.service import AccountAPI, BookAPI
from handlers.web import MainHandler, DevHandler, BookHandler, AuthenticateHandler, LogsHandler

define("port", default=5000, help="run on the given port", type=int)
define("root", default="http://localhost:5000", help="application url")
define("cookie_secret", default="123456", help="application secret cookie")
define('driver_url', default="localhost:27017", help="mongo db driver_url")
define('collection', default="test", help="mongo db collection")
define('douban_app_key', default="appkey", help="your douban app key")
define('douban_app_secret', default="appsecret", help="you douban app secret")
define('douban_callback', default="http://localhost/callback",
       help="you douban app callback url")
define('douban_auth_url', default="http://douban.api/auth",
       help="douban api address to auth")
define('douban_account_info', default="http://douban.api/auth~me",
       help="douban api to get current account info")
# application settings and handle mapping info


def generate_uuid():

    date = datetime.datetime.now()
    return date.strftime("%Y%m%d%Hx%M%S")


class LogoutHandler(BaseHandler):

    # clear the cookie and redirect to home page'
    @tornado.web.authenticated
    def get(self):
            self.clear_cookie("userid")
            self.redirect("/")


class GoogleLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):

    # login with google open id
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.collection = self.settings['db'].account
        if self.get_argument("openid.mode", None):
            user = yield self.get_authenticated_user()
            user['uid'] = generate_uuid()
            user['api'] = 'google'

            # sure account already exist
            search_doc = yield motor.Op(self.collection.find_one, {'api': 'google', 'email': user['email']})
            if search_doc is None:
                arguments = yield motor.Op(self.collection.insert, user)
                app_log.info("mongo.insert new google account");
                self.set_secure_cookie('userid', user['uid'])
            else:
                self.set_secure_cookie('userid', search_doc['uid'])
            # Save the user with with set_secure_cookie()
            self.redirect("/")
        else:
            yield self.authenticate_redirect()


class DoubanSiginHandler(BaseHandler):

    # redirect to douban login page
    def get(self):
        url = options.douban_auth_url + "/auth?response_type=code&client_id=" + \
            options.douban_app_key + "&redirect_uri=" + options.douban_callback
        self.redirect(url)


class DoubanCallbackHandler(BaseHandler):

    # get the params of douban callback
    @tornado.gen.coroutine
    def get(self):
        self.collection = self.settings['db'].account
        code = self.get_argument('code')
        url = douban_auth_url + "/token"
        values = {
            "client_id": options.douban_app_key,
            "client_secret": options.douban_app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": options.douban_callback,
            "code": code
        }
        data = urllib.urlencode(values)

        try:

            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)
            douban_json = json.loads(response.read())

            access_token = douban_json['access_token']
            refresh_token = douban_json['refresh_token']
            # read account info
            request2 = urllib2.Request(options.douban_account_info)
            request2.add_header('Authorization', 'Bearer ' + access_token)
            response2 = urllib2.urlopen(request2)
            account_json = json.loads(response2.read())

            name = account_json['name']
            avatar = account_json['avatar']
            uid = account_json['uid']

            # account info dict save in session
            account = dict(
                uid=uid,
                name=name,
                avatar=avatar,
                access_token=access_token,
                refresh_token=refresh_token,
                api='douban'
            )

            # sure the account is exit in database
            try:
                result = yield motor.Op(self.collection.find_one, {'api': 'douban', 'uid': uid})

                if result is None:
                    # save account info to database
                    arguments = yield motor.Op(self.collection.insert, account)

                else:
                    _id = result['_id']
                    result['access_token'] = access_token
                    result['refresh_token'] = refresh_token
                    update_result = yield motor.Op(self.collection.update, {'_id': _id}, result)
                    # print 'replaced', update_result['n'], 'document'

            except:
                app_log.error('some error happen when query account')

            self.set_secure_cookie("userid", uid)
            self.set_secure_cookie('api', 'douban')
            self.redirect("/")

        except urllib2.URLError, e:
            app_log.error(e)
            self.redirect("/sigin?error=" + e.reason)


class Application(tornado.web.Application):

    def __init__(self):

        client = motor.MotorClient(
            options.driver_url).open_sync()
        db = client[options.collection]

        handlers = [
            (r"/", MainHandler),
            (r"/dev", DevHandler),
            (r"/logs", LogsHandler),
            (r'/contribute', ContributeHandler),
            (r"/sigin", AuthenticateHandler),
            (r"/sigout", LogoutHandler),
            (R"/weixin/service1", WeiXinHandler),
            (r"/sigin/google", GoogleLoginHandler),
            (r"/sigin/douban", DoubanSiginHandler),
            (r"/book/([0-9]+)", BookHandler),
            (r"/callback", DoubanCallbackHandler),
            (r"/api/account/([\s\S]*)", AccountAPI),
            (r"/api/book/search/([\s\S]*)", DoubanSearchHandler),
            (r"/api/book/([0-9]+)", BookAPI)
        ]
        settings = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=options.cookie_secret,
            login_url="/sigin",
            db=db,
            debug=True,
            root=options.root
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():

    conf_file = os.path.join(
        os.path.dirname(__file__), "conf" + os.path.sep + "server.conf")
    tornado.options.parse_config_file(conf_file)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(os.environ.get("PORT", options.port))
    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
