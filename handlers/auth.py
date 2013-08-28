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

from . import BaseHandler

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