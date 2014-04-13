# coding: utf-8
import os
import tornado.web

static_dir = os.path.join(os.path.dirname(__file__), "static")
static_dir_dict = dict(path=static_dir)

router = [
    (r"/(crossdomain\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
    (r"/(humans\.xml)", tornado.web.StaticFileHandler, static_dir_dict),
    (r"/(rebots\.xml)", tornado.web.StaticFileHandler, static_dir_dict)
]