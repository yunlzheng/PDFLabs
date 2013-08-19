# -*- coding: utf-8 -*-
'''
   WeiXinHandler def get to handle the weixing access info
   and the Post get the publish message
'''
import xml.dom.minidom

import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient

class WeiXinHandler(tornado.web.RequestHandler,):

    def get(self):
        self.get_argument('signature', None)
        self.get_argument('timestamp', None)
        self.get_argument('nonce', None)
        echostr = self.get_argument('echostr', '')
        self.write(echostr)

    @tornado.gen.coroutine
    def post(self):
        request_body = self.request.body
        doc = xml.dom.minidom.parseString(request_body)
        toUserName = doc.getElementsByTagName(
            "ToUserName")[0].firstChild.nodeValue
        fromUserName = doc.getElementsByTagName(
            "FromUserName")[0].firstChild.nodeValue
        createTime = doc.getElementsByTagName(
            "CreateTime")[0].firstChild.nodeValue

        response_content = ""

        try:
            # if the event message
            event = doc.getElementsByTagName(
                "Event")[0].firstChild.nodeValue
            msgType = 'text'
            content = '感谢你订阅"墨鱼-cuttle的微信公共帐号beta版（请调戏）\n即将推出的功能关键字："天气"，"搜索"\n回复"?"现实帮助菜单'
        except:
            # else the other messgae
            msgType = doc.getElementsByTagName(
                "MsgType")[0].firstChild.nodeValue
            content = doc.getElementsByTagName(
                "Content")[0].firstChild.nodeValue
            print "###########request ##############"
            content = content.encode('utf8')
            print content
            msgId = doc.getElementsByTagName("MsgId")[0].firstChild.nodeValue

            if content.find("?") != -1 or content.find("？") != -1:
                help_content = "你好，我是墨鱼(Beta)版,功能列表\n"
                help_content += "1 天气查询:输入关键子'天气:城市名'\n"
                help_content += "回复'?' 帮助菜单\n"
                response_content = help_content

            elif content.find("天气") != -1:
                if content.find("：") != -1:
                    wether_data = content.split("：")
                elif content.find(":") != -1:
                    wether_data = content.split(":")

                city = wether_data[1]
                url =  "http://www.webxml.com.cn/WebServices/WeatherWebservice.asmx/getWeatherbyCityName?theCityName=" + \
                    wether_data[1]
                http_client = AsyncHTTPClient()
                weather_response = yield http_client.fetch(url)
                weather_doc = xml.dom.minidom.parseString(
                    weather_response.body)
                weather = weather_doc.getElementsByTagName('string')
                weather_content = ""
                # weather = weather[4:-8]
                del weather[2]
                del weather[2]
                del weather[6]
                del weather[6]         
                for item in weather[0:-10]:
                    weather_content += item.firstChild.nodeValue + "\n"
                weather_content = weather_content.encode('utf8')
                response_content = weather_content
            else:
                response_content = content
        response = '''<xml>
		 <ToUserName><![CDATA[{0}]]></ToUserName>
		 <FromUserName><![CDATA[gh_ca049f6f6b07]]></FromUserName>
		 <CreateTime>12345678</CreateTime>
		 <MsgType><![CDATA[{1}]]></MsgType>
		 <Content><![CDATA[{2}]]></Content>
	        </xml>'''

        response = response.format(
            fromUserName, msgType, response_content)

        self.write(response)
