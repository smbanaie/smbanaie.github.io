#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import string
import os.path
import uuid
import jdatetime
import random



class TornadoRequestBase(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TornadoRequestBase, self).__init__(application, request, **kwargs)




class index_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/index.html')


