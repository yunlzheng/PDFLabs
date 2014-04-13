# -*- coding : utf-8 -*-
from routers.handlers_route import router as handler_routes
from routers.statics_route import router as static_routes

routers = []
routers.extend(static_routes)
routers.extend(handler_routes)