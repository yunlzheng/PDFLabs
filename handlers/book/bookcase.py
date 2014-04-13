# coding: utf-8

from handlers import BaseHandler


class BookcaseHandler(BaseHandler):
    def get(self, *args):
        variables = {
            "page_heading": "分类书架",
            "groups": self.get_groups()
        }
        if self.is_get_collections(*args):
            self.render("book/bookcases.html", **variables)
        else:
            self.render("book/bookcase.html", **variables)


    def is_get_collections(self, *args):
        length = len(args)
        return length == 0
