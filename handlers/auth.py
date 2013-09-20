#!/usr/bin/env python
#*-* coding:utf-8 *-
import datetime
import urllib
import urllib2
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import *

from handlers import BaseHandler
from models.users import User

class UUIDMixin():

    def generate_uuid(self):
        date = datetime.datetime.now()
        return date.strftime("%Y%m%d%Hx%M%S")


class AuthenticateHandler(BaseHandler):

    ''' redirect to the login page '''
    def get(self):
        self.render(
            "sigin.html",
            page_heading='PDFLabs 登录'
        )

    def post(self):
        email = self.get_argument('email').decode()
        password = self.get_argument('password').decode()
        try:
            user = User.objects(email=email, password=password)[0]
            if not user:
                self.redirect('/sigin')
        except Exception as ex:
            app_log.error(ex)
            self.redirect('/sigin')
        else:
            self.set_secure_cookie('userid', user.uid)
            self.redirect('/')


class LogoutHandler(BaseHandler):

    # clear the cookie and redirect to home page'
    @tornado.web.authenticated
    def get(self):
            self.clear_cookie("userid")
            self.redirect("/")


class GoogleLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin, UUIDMixin):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        if self.get_argument("openid.mode", None):

            result = yield self.get_authenticated_user()
            try:
                user = User.objects(type='google', email=result['email'])[0]
            except Exception as ex:
                app_log.error(ex)
                user = User(uid=self.generate_uuid(),
                            type='google',
                            email=result['email'],
                            name=result['name'])
                user.save()

            self.set_secure_cookie('userid', user.uid)
            self.set_secure_cookie('type', 'douban')
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

        code = self.get_argument('code')
        url = options.douban_auth_url + "/token"
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
            data = json.loads(response.read())
            # read account info
            request2 = urllib2.Request(options.douban_account_info)
            request2.add_header('Authorization', 'Bearer ' + access_token)
            response2 = urllib2.urlopen(request2)
            account = json.loads(response2.read())

            try:
                user = User.objects(type='douban', uid=uid)[0]
            except Exception, e:
                app_log.error(e)
                user = User(uid=account_json['uid'],
                        type='douban',
                        name=account['name'],
                        avatar=account['avatar'],
                        access_token=data['access_token'],
                        refresh_token=data['refresh_token'])
            else:
                user.access_token=access_token
                user.refresh_token = refresh_token
            finally:
                user.save()

            self.set_secure_cookie('userid', user.uid)
            self.set_secure_cookie('type', 'douban')
            self.redirect("/")

        except urllib2.URLError, e:
            app_log.error(e)
            self.redirect("/sigin?error=" + e.reason)
