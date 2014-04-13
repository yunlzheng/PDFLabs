# coding=utf-8
import json
import urllib
import urllib2

import tornado
import tornado.gen
from tornado.log import app_log
from tornado.options import options

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

        code = self.get_argument('code')
        if not code:
            # 登录失败跳转到登录页面
            return self.redirect("/sigin")
        url = options.douban_auth_token
        values = {
            "client_id": options.douban_app_key,
            "client_secret": options.douban_app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": options.douban_callback,
            "code": code
        }

        data = urllib.urlencode(values)

        try:
            #TODO ： 修改为异步方法调用
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)
            data = json.loads(response.read())
            access_token = data['access_token']
            refresh_token = data['refresh_token']

            # 根据access_token 获取用户信息
            # TODO : 修改为异步方法调用
            request2 = urllib2.Request(options.douban_account_info)
            request2.add_header('Authorization', 'Bearer ' + data['access_token'])
            response2 = urllib2.urlopen(request2)
            user = self.__build_user_info(response2, access_token, refresh_token)

            try:
                user = User.objects(type='douban', uid=user['uid'])[0]
            except Exception, e:
                app_log.error(e)
            finally:
                user.save()

            self.set_secure_cookie('userid', str(user.id))
            self.set_secure_cookie('type', 'douban')
            self.redirect("/")

        except urllib2.URLError, e:
            app_log.error(e)
            self.redirect("/sigin?error=" + e.reason)

    def __build_user_info(self, response, access_token, refresh_token):
        json_data = json.loads(response.read())
        user = User(
            uid=json_data['uid'],
            type='douban',
            name=json_data['name'],
            avatar=json_data['avatar'],
            access_token=access_token,
            refresh_token=refresh_token
        )
        return user
