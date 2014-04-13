# coding: utf-8
import tornado.websocket
from tornado.log import app_log

__author__ = 'zheng'


class ChartHandler(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        app_log.debug(self)
        self.write_message(u"You said:" + message)

    def write_message(self, message, binary=False):
        super(ChartHandler, self).write_message(message, binary)

    def open(self):
        print "WebSocket Opened"
        super(ChartHandler, self).open()

    def close(self):
        print "WebSocket Closed"
        super(ChartHandler, self).close()




