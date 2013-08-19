# -*- coding : utf-8 -*-
'''
	async the mongodb database and create the data on local
'''
import os
import os.path
import urllib
import pymongo
from pymongo import MongoClient

client = MongoClient(
    "mongodb://cuttle:cuttle@ds037688.mongolab.com:37688/heroku_app17272954")


def main():

    baseurl = "http://cuttle.herokuapp.com/static/doc/"
    db = client['heroku_app17272954']
    collection = db['books']

    for book in collection.find():
        filename = book['id'] + ".pdf"
        swfname = book['id'] + ".swf"
        print book['title'], filename
        if os.path.exists(filename):
            print "exists pass"
        else:
            url = baseurl + book['id'] + '.pdf'
            urllib.urlretrieve(url)

        if os.path.exists(filename):
            if not os.path.exists(swfname):
                response = os.popen("./pdf2swf.sh " + book['id'])
                print response.read()
    print "######################"
    print "#####Async Book Meta Over####"
    print "######################"

    commit()


def commit():
    print ">>>>auto commit the change"
    status = os.popen('git status')
    print status.read(), '\n'
    add = os.popen('git add .')
    print add.read(), '\n'
    commit = os.popen('git commit -m "auto async the book data"')
    print commit.read(), '\n'
    push = os.popen('git push heroku master')
    print push.read()


if __name__ == "__main__":
    main()
