# coding: utf-8
import urllib
import hashlib


def getAvatar(email, default=None, size=100):
    if default:
        return default
    else:
        # construct the url
        name = email.replace("@", "").replace(".", "").strip()[0:1]
        default = "https://identicons.github.com/z{0}.png".format(name)
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url