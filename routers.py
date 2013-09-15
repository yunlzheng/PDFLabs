# -*- coding : utf-8 -*-
from handlers.weixin import WeiXinHandler
from handlers.douban import BookDetailHandler, BookSearchHandler
from handlers.service import AccountAPI, IWantService
from handlers.auth import GoogleLoginHandler, LogoutHandler, DoubanSiginHandler, DoubanCallbackHandler
from handlers.web import MainHandler, DevHandler, AuthenticateHandler, LogsHandler
from handlers.web import BookHandler, PreviewHandler, ContributeHandler

router = [
      (r"/", MainHandler),
      (r"/dev", DevHandler),
      (r"/logs", LogsHandler),
      (r'/contribute', ContributeHandler),
      (r"/book/([0-9]+)", BookHandler),
      (r"/preview/([0-9]+)", PreviewHandler),
      (r"/callback", DoubanCallbackHandler),
      (r"/sigin", AuthenticateHandler),
      (r"/sigout", LogoutHandler),
      (r"/sigin/google", GoogleLoginHandler),
      (r"/sigin/douban", DoubanSiginHandler),
      (r"/api/account/([\s\S]*)", AccountAPI),
      (r"/api/book/search/([\s\S]*)", BookSearchHandler),
      (r"/api/book/([0-9]+)", BookDetailHandler),
      (r"/api/want/([0-9]+)", IWantService),
      (r"/weixin/service1", WeiXinHandler)
]