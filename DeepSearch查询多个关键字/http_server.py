# coding=utf8
from __future__ import unicode_literals

import time
import sys
import json
import os
import base64

import tornado
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.httpclient import AsyncHTTPClient, HTTPClient

from service import ImageSearchService
from service import KeywordSearchService

image_search_service = ImageSearchService()
keyword_search_service = KeywordSearchService()

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(ROOT_PATH + "index.html")


class ImageSearchHandler(tornado.web.RequestHandler):
    def get(self):
        image_id = tornado.escape.xhtml_escape(self.get_argument("image_id")).strip()
        result = image_search_service.search(image_id)
        self.render(ROOT_PATH + "search.html", 
                image_list=result['result'], 
                result_count=len(result['result']),
                result_secs=result['time_secs'],
                image_id=image_id,
                image_size=result['image_size'])


class KeySearchHandler(tornado.web.RequestHandler):
    def get(self):
        keyword =self.get_argument('keyword')
        print keyword
        result = keyword_search_service.search(keyword)
        self.render(ROOT_PATH + "search.html", 
                image_list=result['result'], 
                result_count=len(result['result']),
                result_secs=result['time_secs'],
                image_id=25,
                image_size=result['image_size'])


class ImageUrlSearchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        keyword=self.get_argument("keyword")
        print('%s' % keyword)
        self.redirect('/key?keyword=%s' % keyword)

class ImageUploadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        image = self.request.files['image'][0]['body']
        image_id = image_search_service.save_image(image)
        self.redirect('/search?image_id=%s' % image_id)


if __name__ == "__main__":
    settings = {
        "debug" : True
    }

    ROOT_PATH = "view/"
    IMAGES_PATH = "images/"
    UPLOADS_PATH = "uploads/"
    PORT = 8080

    print 'Deep Search starting at port %d.' % (PORT)
    application = tornado.web.Application([
        (r"/",                      MainPageHandler),
        (r"/search",                ImageSearchHandler),
        (r"/key",                   KeySearchHandler),
        (r"/upload_url",            ImageUrlSearchHandler),
        (r"/upload",                ImageUploadHandler),
        (r"/image/upload/(.+)",     tornado.web.StaticFileHandler, dict(path=UPLOADS_PATH)),
        (r"/image/(.+)",            tornado.web.StaticFileHandler, dict(path=IMAGES_PATH)),
        (r"/(.+)",                  tornado.web.StaticFileHandler, dict(path=ROOT_PATH)),
    ], **settings)
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()