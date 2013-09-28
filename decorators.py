# coding:utf-8
import os
import datetime
import resource
import functools
import traceback
import socket
import urllib
import urlparse

import tornado.web
from tornado.util import import_object
from tornado.log import app_log

def load_model(func):
    """注入一个Model参数给函数."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        #setattr(self, 'session', "session")
        app_log.info('revice request args: {0} kwargs: {1}'.format(args, kwargs))
        model_class = "models.{0}".format(args[0])
        try:
            model = import_object(model_class)
            app_log.info(model)
            setattr(self, 'model', model)
        except Exception as ex:
            app_log.error(ex)
            raise tornado.web.HTTPError(404)
        app_log.info('revice request args: {0} kwargs: {1}'.format(args, kwargs))
        return func(self, *args, **kwargs)
    return wrapper


def log_exception(view_func):
    """ 
    log exception decorator for a view,
    """
    def _decorator(self, *args, **kwargs):
        try:
            response = view_func(self, *args, **kwargs)
        except:
            if self.settings['debug']:
                raise
            tb = traceback.format_exc()
            # get the view name from request
            log_dict = { 'class_method':"%s.%s" % (self.__class__.__module__, self.__class__.__name__),
                         'method':self.request.method,
                         'url':self.request.full_url(),
                         'remote':self.request.remote_ip,
                         'tb':tb,
                         'date':datetime.datetime.utcnow(),
                         'tb_short':tb.splitlines()[-1],
                         'hostname':socket.gethostname(),
                         'pid':int(os.getpid()),
                         'rss':int(resource.getrusage(resource.RUSAGE_SELF)[2])
                         }
            if getattr(self, 'current_user', None):
                #log_dict['user'] = g.current_user
                pass
            if len(self.request.arguments) > 0:
                form = ""
                for key in self.request.arguments.keys():
                    form += '%s=\"%s\"\n' % (key,self.request.arguments[key])
                log_dict['form'] = form
 
            try:
                #res = self.db.log.save(log_dict)
                app_log.error(log_dict)
            #except PyMongoError:
            except:
                print (log_dict)
            raise
        return response
    return functools.wraps(view_func)(_decorator)

def authenticated(method):
    """
    自定义登录验证
    @param method:
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            if self.request.method in ("GET", "POST"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri

                    url += "?" + urllib.urlencode(dict(next=next_url))
                self.redirect(url)
            raise tornado.web.HTTPError(403)
            return
        else:
            return method(self, *args, **kwargs)

    return wrapper