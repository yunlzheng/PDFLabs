# -*- coding : utf-8 -*-
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncTestCase

class MyTestCase(AsyncTestCase):
    def test_http_fetch(self):
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch('http://www.tornadoweb.org')
        # Test contents of response
        self.assertIn("FirendFeed", response.body)

