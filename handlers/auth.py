#*-* coding:utf-8 *-

import datetime
import json
import urllib
import urllib2
import urlparse
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.auth
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient

from handlers import BaseHandler
from models.users import User
from util.gravatar import getAvatar


def callback(_dict):
    """
    QQ 登录根据openid获取当前登录用户信息时，返回的为jsonp，
    使用 eval("callback(str)") 获取返回值
    @param _dict:
    @return: dict
    """
    return _dict


class UUIDMixin():

    def __init__(self):
        pass

    def generate_uuid(self):
        date = datetime.datetime.now()
        return date.strftime("%Y%m%d%Hx%M%S")


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
            user = User.objects(email=email, password=password)[0]
            if not user:
                self.redirect('/sigin')
        except Exception as ex:
            app_log.error(ex)
            self.redirect('/sigin')
        else:
            self.set_secure_cookie('userid', str(user.id))
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
                            name=result['name'],
                            avatar=getAvatar('email')
                            )
                user.save()

            self.set_secure_cookie('userid', str(user.id))
            self.set_secure_cookie('type', 'google')
            self.redirect("/")
        else:
            yield self.authenticate_redirect()


class DoubanSiginHandler(BaseHandler):

    def get(self):
        """
        跳转到豆瓣登录页面
        """
        url = options.douban_auth_url + "?response_type=code&client_id=" + \
            options.douban_app_key + "&redirect_uri=" + options.douban_callback
        self.redirect(url)


class DoubanCallbackHandler(BaseHandler):

    # get the params of douban callback
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


class TencentSiginHandler(BaseHandler):


    @tornado.gen.coroutine
    def get(self):
        """
        用户使用QQ第三方登录，获取登录地址并跳转
        """
        request_url = self.__build_auth_url()
        app_log.info("tencent auth_code: {0}".format(request_url))
        self.redirect(request_url)

    def __build_auth_url(self):
        """
        生成QQ登录地址
        @return: 用户QQ登录的跳转地址
        """
        auth_url = options.qq_auth_url
        params = {
             "response_type": "code",
             "client_id": options.qq_app_key,
             "redirect_uri": options.qq_callback,
             "state": "pdflabs"
        }
        params = urllib.urlencode(params)
        request_url = auth_url+"?"+params
        return request_url


class TencentSiginCallbackHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        async_client = AsyncHTTPClient()
        auth_code = self.get_argument("code",None)
        if auth_code:
            # 第一步 获取access_token
            auth_token_url = self.__build_auth_token_url(auth_code)
            token_response =yield async_client.fetch(auth_token_url)
            access_token,refresh_token = self.__parse_token(token_response)

            # 第二不 得到用户身份信息
            auth_me_url = self.__build_auth_me_url(access_token)
            open_response = yield async_client.fetch(auth_me_url)
            openid = self.__parse_me(open_response)

            # 第三布 获取用户基本信息
            auth_user_url = self.__build_auth_user_url(access_token, openid)
            user_info = yield async_client.fetch(auth_user_url)
            user = self.__parse_user(user_info, access_token, refresh_token, openid)
            # 确认用户是否已经登录过
            try:
                user = User.objects(type='qq', uid=openid)[0]
            except Exception as ex:
                app_log.exception(ex)
            finally:
                user.save()
                self.set_secure_cookie('userid', str(user.id))
                self.set_secure_cookie('type', 'qq')
                self.redirect("/")
        else:
            # 登录失败，跳转到登录页面
            self.redirect("/sigin")

    def __build_auth_token_url(self, auth_code):
        """
        生成获取access_token的url地址
        """
        token_url = options.qq_auth_token
        params = dict(
            grant_type="authorization_code",
            client_id=options.qq_app_key,
            client_secret=options.qq_app_secret,
            code=auth_code,
            redirect_uri=options.qq_callback
        )
        params = urllib.urlencode(params)
        request_url = token_url+"?"+params
        return request_url

    def __build_auth_me_url(self, access_token):
        """
        生成获取用户openid的url地址
        """
        auth_me_url = options.qq_auth_me+"?access_token="+str(access_token)
        return auth_me_url

    def __build_auth_user_url(self, access_token, openid):
        """
        生成根据penid 获取生成QQ用户信息的url地址
        """
        auth_user_url = options.qq_auth_user+"?" \
                            "access_token="+access_token+"" \
                            "&oauth_consumer_key=100530962" \
                            "&openid="+str(openid)
        return auth_user_url

    def __parse_token(self, http_response):
        """
        解析返回的access_token, 和 refresh_token
        @param http_response:
        @return:
        """
        query_str = urllib.unquote(http_response.body)
        params = urlparse.parse_qs(query_str)
        access_token = params['access_token'][0]
        refresh_token = params['refresh_token'][0]
        return (access_token, refresh_token)

    def __parse_me(self, http_response):
        """
        解析获取用户QQ的openid
        @param http_response:
        """
        evel_str = http_response.body.strip()[0:-1]
        _dic = eval(evel_str)
        return _dic.get('openid')

    def __parse_user(self, http_response, access_token, refresh_token, open_id):

        user_info = json.loads(http_response.body)
        user = User(
            uid=open_id,
            type='qq',
            email='',
            name=user_info.get('nickname'),
            avatar=user_info.get('figureurl_qq_2'),
            access_token=access_token,
            refresh_token=refresh_token
        )
        return user