# -*- coding:utf-8 -*-
import qrcode

text = raw_input('enter book id:')


img = qrcode.make("cuttle.herokuapp.com/book/"+text)
img.save(text+'.png')

