# -*- coding : utf-8 -*-
import formencode
from formencode import validators


class WantSchema(formencode.Schema):
    book_id = validators.String(not_empty=True)


class BookSearchSchema(formencode.Schema):
    keyword = validators.String(not_empty=True)


class GreetSchema(formencode.Schema):
    filter_extra_fields = True

    name = validators.String(not_empty=True)