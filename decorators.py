# coding:utf-8
import os
import datetime
import resource
import functools
import traceback
import socket
from tornado.log import app_log

def log_exception(view_func):
    """ log exception decorator for a view,
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