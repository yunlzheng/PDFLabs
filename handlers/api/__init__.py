# coding: utf-8

import json

import tornado.web
from tornado.log import app_log

from .book import IWantApi
from .book import LikeApiHandler
from .book import BookDetailHandler
from .book import BookSearchHandler
from .weixin import WeiXinHandler
from decorators import load_model


__author__ = 'zheng'


class Page(object):
    def __init__(self, skip=None, limit=None):
        self._skip = skip
        self._limit = limit

    @property
    def availiable(self):
        if self._skip and self._limit:
            return True
        return False

    @property
    def skip(self):
        return int(self._skip)

    @property
    def limit(self):
        return int(self._limit)


class BackboneHandler(tornado.web.RequestHandler):
    model = None

    def initialize(self, auth=False):
        self.auth = auth

    def prepare(self):
        if self.auth:
            if not self.current_user:
                raise tornado.web.HTTPError(403)

    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)

    def get(self, *args):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        if self.is_get_collection(*args):
            self.write(self.encode(self.get_collection(*args)))
        else:
            self.write(self.encode(self.get_model(*args)))

    def post(self, *args):
        resp = self.encode(self.create_model(*args))
        self.write(resp)

    def put(self, *args):
        resp = self.encode(self.update_model(*args))
        self.write(resp)

    def delete(self, *args):
        self.delete_model(*args)

    def is_get_collection(self, *args):
        return len(args) == 1

    def get_params(self, *args):
        query = {}
        arguments = self.request.arguments.copy()
        arguments.pop('skip', None)
        arguments.pop('limit', None)
        for key in arguments.keys():
            query[key] = self.get_argument(key)
        return query

    def get_page_params(self, *args):
        skip = self.get_argument('skip', None)
        limit = self.get_argument('limit', None)
        return Page(skip=skip, limit=limit)

    def create_model(self, obj, *args):
        raise tornado.web.HTTPError(404)

    def get_collection(self, *args):
        raise tornado.web.HTTPError(404)

    def get_model(self, *args):
        raise tornado.web.HTTPError(404)

    def update_model(self, obj, *args):
        raise tornado.web.HTTPError(404)

    def delete_model(self, *args):
        raise tornado.web.HTTPError(404)


class MongoBackboneHandler(BackboneHandler):
    def encode(self, data):
        return data.to_json()

    @load_model
    def get_model(self, *args):
        try:
            instance = self.model.objects(id=args[1])[0]
        except Exception as ex:
            app_log.error(ex)
            raise tornado.web.HTTPError(404)
        else:
            return instance

    @load_model
    def get_collection(self, *args):

        query = self.get_params()
        print query
        page = self.get_page_params()
        if page.availiable:
            result = self.model.objects.skip(page.skip).limit(page.limit).filter(**query)
            return result
        else:
            return self.model.objects().filter(**query)

    @load_model
    def delete_model(self, *args):
        try:
            instance = self.model.objects(id=args[1]).first()
            instance.delete()
        except Exception, e:
            raise e
        else:
            return instance

    @load_model
    def create_model(self, *args):
        #print obj
        obj = self.decode(self.request.body)
        obj = self.model(**obj)
        obj.save()
        return obj

    @load_model
    def update_model(self, *args):
        obj = self.decode(self.request.body)
        instance = self.model.objects(id=args[1]).first()
        for key in obj:
            if hasattr(instance, key):
                setattr(instance, key, obj[key])
        instance.save()
        return instance