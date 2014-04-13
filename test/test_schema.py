# -*- coding : utf-8 -*-
from validate import validate
from schema import GreetSchema


class TestSchema():
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @validate(GreetSchema)
    def greet(self, name):
        print 'hello', name

    def testGreetSchema(self):
        try:
            self.greet(name='xxxxxx')
        except Exception as ex:
            print ex