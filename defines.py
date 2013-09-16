#!/usr/bin/env python
#*-* coding:utf-8 *-
from tornado.options import define

define("port", default=5000, help="run on the given port", type=int)
define("root", help="application url")
define("cookie_secret", help="application secret cookie")
define('driver_url', help="mongo db driver_url")
define('database', default="test", help="mongo db collection")
define('douban_app_key',  help="your douban app key")
define('douban_app_secret', help="you douban app secret")
define('douban_callback',  help="you douban app callback url")
define('douban_auth_url', help="douban api address to auth")
define('douban_account_info',  help="douban api to get current account info")

define('mongo_host', default='ds041198.mongolab.com')
define('mongo_port', default=41198, type=int)
define('mongo_username', default='zheng')
define('mongo_password', default='123456')