# coding: utf-8
import urllib, hashlib

def getAvatar(email):
    default = "http://pdflabs.herokuapp.com/static/images/avatar.jpg"
    size = 100
    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url