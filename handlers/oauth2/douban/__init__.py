# coding=utf-8
import json
import urllib

import tornado
import tornado.gen
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError

from handlers import BaseHandler
from models.users import User


class DoubanSiginHandler(BaseHandler):
    """
    跳转到豆瓣登录页面
    """

    def get(self):
        url = options.douban_auth_url + "?response_type=code&client_id=" + \
              options.douban_app_key + "&redirect_uri=" + options.douban_callback
        self.redirect(url)


class DoubanCallbackHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        async_client = AsyncHTTPClient()
        code = self.get_argument('code')
        if not code:
            try:
                auth_token_url = self.__build_auth_token_url(code)
                token_response = yield async_client.fetch(auth_token_url)
                data = json.loads(token_response.body)
                access_token = data['access_token']
                refresh_token = data['refresh_token']

                # 根据access_token 获取用户信息
                auth_response = yield async_client.fetch(self.__build_auth_user_request(access_token))
                user = self.save_douban_user(self.__build_user_info(auth_response, access_token, refresh_token))
                self.set_secure_cookie('userid', str(user.id))
                self.set_secure_cookie('type', 'douban')
                self.redirect("/")

            except HTTPError, e:
                app_log.error(e)
                self.redirect("/sigin?error=" + e.message)
        else:
            self.redirect("/sigin")

    @staticmethod
    def save_douban_user(user):
        try:
            user = User.objects(type='douban', uid=user['uid'])[0]
        except Exception, e:
            app_log.error(e)
        finally:
            user.save()
        return user

    @staticmethod
    def __build_auth_token_url(auth_code):
        token_url = options.douban_auth_token
        params = {
            "client_id": options.douban_app_key,
            "client_secret": options.douban_app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": options.douban_callback,
            "code": auth_code
        }
        params = urllib.urlencode(params)
        request_url = token_url + "?" + params
        return request_url

    @staticmethod
    def __build_auth_user_request(access_token):
        httprequest = HTTPRequest(options.douban_auth_user)
        httprequest.headers = {
            "Authorization": 'Bearer ' + access_token
        }
        return httprequest

    @staticmethod
    def __build_user_info(response, access_token, refresh_token):
        json_data = json.loads(response.body)
        user = User(
            uid=json_data['uid'],
            type='douban',
            name=json_data['name'],
            avatar=json_data['avatar'],
            access_token=access_token,
            refresh_token=refresh_token
        )
        return user
