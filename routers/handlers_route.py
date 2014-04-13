# coding: utf-8
from handlers import MainHandler
from handlers.web import LogsHandler
from handlers.web import AdminHandler
from handlers.user import UserHandler
from handlers.book import PreviewHandler
from handlers.book import BookHandler
from handlers.book import BooksHandler
from handlers.book import FindHandler
from handlers.book import BookcaseHandler
from handlers.group import GroupHandler
from handlers.group import PostHandler
from handlers.funny import UserGalleryHandler, UserGalleryApiHandler
from handlers.api import IWantApi
from handlers.api import LikeApiHandler
from handlers.api import BookDetailHandler, BookSearchHandler
from handlers.api import WeiXinHandler
from handlers.api import MongoBackboneHandler
from handlers.chart import ChartHandler
from handlers.auth import AuthenticateHandler
from handlers.auth import GoogleLoginHandler
from handlers.oauth2.douban import DoubanSiginHandler, DoubanCallbackHandler
from handlers.oauth2.tencent import TencentSiginHandler, TencentSiginCallbackHandler
from handlers.auth import LogoutHandler

router = [
    (r"/", MainHandler),
    (r"/admin", AdminHandler),
    (r"/websocket", ChartHandler),
    (r"/logs", LogsHandler),
    (r'/users/(.+)', UserHandler),
    (r'/gallery', UserGalleryHandler),
    (r"/gallery/api", UserGalleryApiHandler),
    (r'/book/find', FindHandler),
    (r"/book", BooksHandler),
    (r"/book/([0-9]+)", BookHandler),
    (r"/book/preview/([0-9]+)", PreviewHandler),
    (r"/bookcases", BookcaseHandler),
    (r"/bookcases/([0-9a-zA-Z\-]+)", BookcaseHandler),
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