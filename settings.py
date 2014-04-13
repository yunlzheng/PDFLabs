# coding: utf-8
import os.path

###### application setting
PORT = 5000
DOMAIN_NAME = "http://pdflabs.herokuapp.com"
COOKIE_SECRET = "1234567890"
LOGIN_URL = "/sigin"
DEBUG = True
PROJECT_PATH = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, "templates")
STATIC_PATH = os.path.join(PROJECT_PATH, "static")

###### database setting
#MONGO_DRIVER_URL = "mongodb://localhost:27017"
MONGO_DRIVER_URL = "mongodb://zheng:123456@ds041198.mongolab.com:41198/heroku_app17595021"
MONGO_COLLECTION = "heroku_app17595021"

###### douban oauth2 setting
DOUBAN_APP_KEY = "05a682aac674d51a10f38800535e7f4e"
DOUBAN_APP_SECRET = "1b86275dcc1c5946"
# 豆瓣登录的跳转地址
DOUBAN_AUTH_URL = "https://www.douban.com/service/auth2/auth"
# 豆瓣用户登录完成后的回调地址 并返回 auth_code信息
DOUBAN_CALLBACK = "http://pdflabs.herokuapp.com/callback"
# 获取豆瓣用户的access_token
DOUBAN_AUTH_TOKEN = "https://www.douban.com/service/auth2/token"
# 利用access_token 获取用户的详细信息
DOUBAN_AUTH_USER = "https://api.douban.com/v2/user/~me"


###### qq oauth2
QQ_APP_KEY = "100530962"
QQ_APP_SECRET = "9140d3715d634c9917f84b9f6982bf53"
# QQ 登录跳转地址
QQ_AUTH_URL = "https://graph.qq.com/oauth2.0/authorize"
# 登录完成后的回调地址 返回auth_code
QQ_CALLBACK = "http://pdflabs.herokuapp.com/callback/qq"
# 根据获取的auth_code 获取access_token
QQ_AUTH_TOKEN = "https://graph.qq.com/oauth2.0/token"
# 根据access_token 得到用户的身份信息 openid
QQ_AUTH_ME = "https://graph.qq.com/oauth2.0/me"
# 根据获取到的openid 和 access_token获取用户的详细信息
QQ_AUTH_USER = "https://graph.qq.com/user/get_user_info"

##### weib oauth2 setting