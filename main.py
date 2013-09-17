#!/usr/bin/env python
#*-* coding:utf-8 *-

#	Sample main.py Tornado file
#
#	Author: Zheng yunlong
#
import os
import os.path

import motor
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.options
import tornado.web
import tornado.auth

from tornado.log import app_log
from tornado.options import options

import defines
from routers import router


# application settings and handle mapping info

class Application(tornado.web.Application):

    def __init__(self):

        client = motor.MotorClient(
            options.driver_url).open_sync()

        db = client[options.database]

        static_dir = os.path.join(os.path.dirname(__file__), "static")

        handlers = router
        settings = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), "templates"),
            static_path= static_dir,
            cookie_secret=options.cookie_secret,
            login_url="/sigin",
            db=db,
            debug=True,
            root=options.root
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    conf_file = os.path.join(os.path.dirname(__file__), "conf" + os.path.sep + "server.conf")
    tornado.options.parse_config_file(conf_file)
    app_log.info(' PDFLabs running server on {0}'.format(options.port))
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(os.environ.get("PORT", options.port))
    tornado.ioloop.IOLoop.instance().start()
