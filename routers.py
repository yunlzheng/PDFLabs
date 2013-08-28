# -*- coding : utf-8 -*-
from handlers import *
from handlers.weixin import WeiXinHandler
from handlers.service import AccountAPI, BookAPI
from handlers.web import MainHandler, DevHandler, BookHandler, AuthenticateHandler, LogsHandler

router = [
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