# -*- coding : utf-8 -*-

import tornado.web

class EditorModule(tornado.web.UIModule):
    def render(self):
        return self.render_string(
            "module/editor.html"
        )
