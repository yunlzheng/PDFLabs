#*-* coding:utf-8 *-
from uuid import uuid4

import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.auth
from tornado.log import app_log

from handlers import BaseHandler
from models.users import User
from util.gravatar import getAvatar


class AuthenticateHandler(BaseHandler):
    def get(self):
        """
        跳转到登录页面
        """
        self.render(
            "sigin.html",
            page_heading='PDFLabs 登录'
        )

    def post(self):
        email = self.get_argument('email').decode()
        password = self.get_argument('password').decode()
        try:
            user = User.objects(email=email, password=password).first()
            if not user:
                self.redirect('/sigin')
        except Exception as ex:
            app_log.error(ex)
            self.redirect('/sigin')
        else:
            self.set_secure_cookie('userid', str(user.id))
            self.set_secure_cookie('admin', "True")
            try:
                next_url = self.get_argument('next')
                if next_url:
                    self.redirect(next_url)
                    return
                self.redirect('/')
            except Exception as ex:
                app_log.exception(ex)
                self.redirect('/')


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        """
        退出登录，清除当前cookie值

        """
        self.clear_cookie("userid")
        self.clear_cookie('admin')
        self.redirect("/")


class GoogleLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        if self.get_argument("openid.mode", None):

            result = yield self.get_authenticated_user()
            try:
                user = User.objects(type='google', email=result['email'])[0]
            except Exception as ex:
                app_log.error(ex)
                user = User(uid=str(uuid4()),
                            type='google',
                            email=result['email'],
                            name=result['name'],
                            avatar=getAvatar('email')
                )
                user.save()

            self.set_secure_cookie('userid', str(user.id))
            self.set_secure_cookie('type', 'google')
            self.redirect("/")
        else:
            yield self.authenticate_redirect()

