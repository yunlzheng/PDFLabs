# -*- coding : utf-8 -*-
from handlers.weixin import WeiXinHandler
from handlers.douban import BookDetailHandler, BookSearchHandler
from handlers.service import AccountAPI
from handlers.auth import GoogleLoginHandler, LogoutHandler, DoubanSiginHandler, DoubanCallbackHandler
from handlers.web import MainHandler, DevHandler, BookHandler, AuthenticateHandler, LogsHandler, ContributeHandler

router = [
      (r"/", MainHandler),
      (r"/dev", DevHandler),
      (r"/logs", LogsHandler),
      (r'/contribute', ContributeHandler),
      (r"/book/([0-9]+)", BookHandler),
      (r"/callback", DoubanCallbackHandler),
      (r"/sigin", AuthenticateHandler),
      (r"/sigout", LogoutHandler),
      (r"/sigin/google", GoogleLoginHandler),
      (r"/sigin/douban", DoubanSiginHandler),
      (r"/api/account/([\s\S]*)", AccountAPI),
      (r"/api/book/search/([\s\S]*)", BookSearchHandler),
      (r"/api/book/([0-9]+)", BookDetailHandler),
      (r"/weixin/service1", WeiXinHandler)
]