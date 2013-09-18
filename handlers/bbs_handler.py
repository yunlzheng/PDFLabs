# -*- coding : utf-8 -*-

from models.bbs import Bbs
from handlers import BaseHandler

class BbsHandler(BaseHandler):

    def get(self, tag):
        bbs = Bbs.objects(tag = tag)[0]
        self.render(
            "bbs.html",
            page_heading=bbs.name,
            bbs = bbs,
            bbss = self.get_bbs()
        )
