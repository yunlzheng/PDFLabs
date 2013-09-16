# -*- coding : utf-8 -*-
from tornado.options import options

from mongoengine import connect

connect(options.database, 
	host=options.mongo_host, 
	port=options.mongo_port, 
	username=options.mongo_username, 
	password=options.mongo_password)