# coding : utf-8
import json
import tornado.web
from tornado.log import app_log

from .user import UserAPI
from .book import IWantApi
from .book import LikeApiHandler
from .book import BookApiHandler
from .book import BookDetailHandler
from .book import BookSearchHandler
from .weixin import WeiXinHandler

from decorators import load_model

class BackboneHandler(tornado.web.RequestHandler):

	def initialize(self, auth= False):
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
		if self.is_get_collection(*args):
			self.write(self.encode(self.get_collection(*args)))
		else:
			self.write(self.encode(self.get_model(*args)))

	def post(self, *args):
		model = self.decode(self.request.body)
		resp = self.create_model(model, *args)
		self.write(resp)

	def put(self, *args):
		model = self.decode(self.request.body)
		resp = self.update_model(model, *args)
		self.write(resp)

	def delete(self, *args):
		self.delete_model(*args)

	def is_get_collection(self, *args):
		return len(args) == 1

	def create_model(self, model, * args):
		raise tornado.web.HTTPError(404)

	def get_collection(self, *args):
		raise tornado.web.HTTPError(404)

	def get_model(self, *args):
		raise tornado.web.HTTPError(404)

	def update_model(self, model, *args):
		raise tornado.web.HTTPError(404)

	def delete_model(self, * args):
		raise tornado.web.HTTPError(404)

class MongoBackboneHandler(BackboneHandler):

	def encode(self,data):
		result = {}
		if isinstance(data, self.model):
			result['data'] = data.to_json()
		else:
			resp = [obj.to_json() for obj in data]
			result['data'] = resp
		return result

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
		return self.model.objects()