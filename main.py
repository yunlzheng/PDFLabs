#*-* coding:utf-8 *-*
#	Sample main.py Tornado file
#
#	Author: Zheng yunlong
#
import os
from os.path import abspath, dirname
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.auth

from tornado.log import app_log
from tornado.options import options, define
from mongoengine import connect

from routers import router as handlers
from handlers.uimodules.editor import EditorModule
import settings


define("port", default=settings.PORT, type=int)
define("domain_name", default=settings.DOMAIN_NAME)
define('static_path', default=settings.STATIC_PATH)
define('template_path', default=settings.TEMPLATE_PATH)
define("cookie_secret", default=settings.COOKIE_SECRET)
define("login_url", default=settings.LOGIN_URL)
define('debug', default=settings.DEBUG)

define('mongo_driver_url', default=settings.MONGO_DRIVER_URL)
define('mongo_collection', default=settings.MONGO_COLLECTION)
define('douban_app_key', default=settings.DOUBAN_APP_KEY)
define('douban_app_secret', default=settings.DOUBAN_APP_SECRET)
define('douban_callback',  default=settings.DOUBAN_CALLBACK)
define('douban_auth_url', default=settings.DOUBAN_AUTH_URL)
define('douban_auth_token', default=settings.DOUBAN_AUTH_TOKEN)
define('douban_auth_user', default=settings.DOUBAN_AUTH_USER)

define('qq_app_key', default=settings.QQ_APP_KEY)
define('qq_app_secret', default=settings.QQ_APP_SECRET)
define('qq_auth_url', default=settings.QQ_AUTH_URL)
define('qq_callback', default=settings.QQ_CALLBACK)
define('qq_auth_token', default=settings.QQ_AUTH_TOKEN)
define('qq_auth_me', default=settings.QQ_AUTH_ME)
define('qq_auth_user', default=settings.QQ_AUTH_USER)

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, 'conf')
CONF_FILE = CONF_DIR+os.path.sep+"application.conf"


class Application(tornado.web.Application):

    def __init__(self):

        connect(options.mongo_collection, host=options.mongo_driver_url)
        settings = dict(
            template_path=options.template_path,
            static_path= options.static_path,
            cookie_secret=options.cookie_secret,
            login_url=options.login_url,
            debug=options.debug,
            domain_name=options.domain_name,
            ui_modules = {'Editor': EditorModule}
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_config_file(CONF_FILE)
    port = os.environ.get("PORT", options.port)
    app_log.debug('PDFLabs running server on {0}'.format(port))
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
