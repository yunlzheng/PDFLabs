# -*- coding : utf-8 -*-
import os
import os.path

import tornado.web

from handlers import MainHandler
from handlers.web import  LogsHandler
from handlers.user import UserHandler
from handlers.book import PreviewHandler
from handlers.book import BookHandler
from handlers.book import BooksHandler
from handlers.book import FindHandler
from handlers.group import GroupHandler
from handlers.group import PostHandler
from handlers.api import IWantApi
from handlers.api import LikeApiHandler
from handlers.api import BookDetailHandler, BookSearchHandler
from handlers.api import WeiXinHandler
from handlers.api import MongoBackboneHandler

from handlers.chart import ChartHandler

from handlers.auth import AuthenticateHandler
from handlers.auth import GoogleLoginHandler
from handlers.auth import DoubanSiginHandler, DoubanCallbackHandler
from handlers.auth import TencentSiginHandler, TencentSiginCallbackHandler
from handlers.auth import LogoutHandler

static_dir = os.path.join(os.path.dirname(__file__), "static")
static_dir_dict = dict(path=static_dir)

router = [
      # static file
      (r"/(crossdomain\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      (r"/(humans\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      (r"/(rebots\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
      # handlers
      (r"/", MainHandler),
      (r"/websocket", ChartHandler),
      (r"/logs", LogsHandler),
      (r'/users/(.+)', UserHandler),
      (r'/book/find', FindHandler),
      (r"/book", BooksHandler),
      (r"/book/([0-9]+)", BookHandler),
      (r"/book/preview/([0-9]+)", PreviewHandler),
      (r"/group/([0-9a-zA-Z\-]+)", GroupHandler),
      (r"/group/([0-9a-zA-Z\-]+)/([0-9a-zA-Z\-]+)", PostHandler),
      (r"/api/book/search/([\s\S]*)", BookSearchHandler),
      (r"/api/book/([0-9]+)", BookDetailHandler),
      (r"/api/want/([0-9]+)", IWantApi),
      (r"/api/like/([0-9]+)", LikeApiHandler),
      (r"/api/rest/([a-z]+)", MongoBackboneHandler),
      (r"/api/rest/([a-z]+)/(.+)", MongoBackboneHandler),
      (r"/sigin", AuthenticateHandler),
      (r"/sigout", LogoutHandler),
      (r"/sigin/google", GoogleLoginHandler),
      (r"/sigin/douban", DoubanSiginHandler),
      (r"/callback", DoubanCallbackHandler),
      (r"/sigin/qq", TencentSiginHandler),
      (r"/callback/qq", TencentSiginCallbackHandler),
      (r"/weixin/service1", WeiXinHandler)
]
