# -*- coding : utf-8 -*-
import os
import os.path

import tornado.web

from handlers.weixin import WeiXinHandler
from handlers.douban import BookDetailHandler, BookSearchHandler
from handlers.auth import GoogleLoginHandler, LogoutHandler, DoubanSiginHandler, DoubanCallbackHandler
from handlers import MainHandler
from handlers.web import  AuthenticateHandler, LogsHandler
from handlers.web import PreviewHandler
from handlers.book import BookHandler
from handlers.book import BooksHandler
from handlers.book import FindHandler
from handlers.group import GroupHandler
from handlers.group import PostHandler
from handlers.api import UserAPI
from handlers.api import IWantApi

static_dir = os.path.join(os.path.dirname(__file__), "static")
static_dir_dict = dict(path=static_dir)

router = [
      # static file
      (r"/(crossdomain\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      (r"/(humans\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      (r"/(rebots\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      # handlers
      (r"/", MainHandler),
      (r"/logs", LogsHandler),
      (r'/book/find', FindHandler),
      (r"/book", BooksHandler),
      (r"/book/([0-9]+)", BookHandler),
      (r"/group/([0-9a-zA-Z\-]+)", GroupHandler),
      (r"/group/([0-9a-zA-Z\-]+)/([0-9a-zA-Z\-]+)", PostHandler),
      (r"/api/account/([\s\S]*)", UserAPI),
      (r"/api/book/search/([\s\S]*)", BookSearchHandler),
      (r"/api/book/([0-9]+)", BookDetailHandler),
      (r"/api/want/([0-9]+)", IWantApi),
      (r"/preview/([0-9]+)", PreviewHandler),
      (r"/callback", DoubanCallbackHandler),
      (r"/sigin", AuthenticateHandler),
      (r"/sigout", LogoutHandler),
      (r"/sigin/google", GoogleLoginHandler),
      (r"/sigin/douban", DoubanSiginHandler),
      (r"/weixin/service1", WeiXinHandler)

]
