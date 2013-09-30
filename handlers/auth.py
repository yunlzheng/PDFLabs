#*-* coding:utf-8 *-
import datetime
import json
import urllib
import urllib2
import urlparse
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.log import app_log
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient

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
            self.set_secure_cookie('userid', str(user.id))
            try:
                next = self.get_argument('next')
                if next:
                    self.redirect(next)
                    return
                self.redirect('/')
            except Exception as ex:
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

            self.set_secure_cookie('userid', str(user.id))
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
            request2.add_header('Authorization', 'Bearer ' + data['access_token'])
            response2 = urllib2.urlopen(request2)
            account = json.loads(response2.read())

            try:
                user = User.objects(type='douban', uid=account['uid'])[0]
            except Exception, e:
                app_log.error(e)
                user = User(uid=account['uid'],
                        type='douban',
                        name=account['name'],
                        avatar=account['avatar'],
                        access_token=data['access_token'],
                        refresh_token=data['refresh_token'])
            else:
                user.access_token=data['access_token']
                user.refresh_token=data['refresh_token']
            finally:
                user.save()

            self.set_secure_cookie('userid', str(user.id))
            self.set_secure_cookie('type', 'douban')
            self.redirect("/")

        except urllib2.URLError, e:
            app_log.error(e)
            self.redirect("/sigin?error=" + e.reason)


class TencentSiginHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        auth_url = "https://graph.qq.com/oauth2.0/authorize"
        params = dict(
             response_type="code",
             client_id="100530962",
             redirect_uri = "http://pdflabs.herokuapp.com/callback/qq",
             state = "pdflabs"
        )

        params = urllib.urlencode(params)

        request_url = auth_url+"?"+params

        app_log.info("tencent auth_code: {0}".format(request_url))
        self.redirect(request_url)

def callback(str):
    return str

class TencentSiginCallbackHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        auth_code = self.get_argument("code",None)
        token_url = "https://graph.qq.com/oauth2.0/token"
        if auth_code:

            # 第一步 获取access_token
            params = dict(
                grant_type="authorization_code",
                client_id="100530962",
                client_secret="9140d3715d634c9917f84b9f6982bf53",
                code=auth_code,
                redirect_uri= "http://pdflabs.herokuapp.com/callback/qq"
            )
            params = urllib.urlencode(params)
            request_url = token_url+"?"+params
            async_client = AsyncHTTPClient()
            response =yield async_client.fetch(request_url)
            query_str = urllib.unquote(response.body)
            params = urlparse.parse_qs(query_str)

            access_token = params['access_token'][0]
            refresh_token = params['refresh_token'][0]
            # 第二不 得到用户身份信息
            open_url = "https://graph.qq.com/oauth2.0/me?access_token="+str(access_token)
            open_response = yield async_client.fetch(open_url)
            evel_str = open_response.body.strip()[0:-1]
            _dic = eval(evel_str)
            openid = _dic.get('openid')


            # 第三布 获取用户基本信息
            user_info_url = "https://graph.qq.com/user/get_user_info?" \
                            "access_token="+access_token+"" \
                            "&oauth_consumer_key=100530962" \
                            "&openid="+str(openid)

            user_info = yield async_client.fetch(user_info_url)

            user_info = json.loads(user_info.body)

            # 确认用户是否已经登录过
            try:
                user = User.objects(type='qq', uid=openid)[0]
                user.avatar = user_info.get('figureurl_qq_2')
            except Exception as ex:
                user = User(uid=openid,
                            type='qq',
                            email='',
                            name=user_info.get('nickname'),
                            avatar=user_info.get('figureurl_qq_2'),
                            access_token=access_token,
                            refresh_token=access_token
                )
            finally:
                user.save()
                self.set_secure_cookie('userid', str(user.id))
                self.set_secure_cookie('type', 'qq')
                self.redirect("/")
        else:
            self.redirect("/sigin")