# -*- coding: gb2312

import os
import httplib
import urllib
import urllib2

class Browser(object):
    pass

class HTTPBrowser(httplib.HTTPConnection):
    header = {}
    cookies = {}
    method = ""
    params = ""
    pass

class HTTPSBrowser(httplib.HTTPSConnection):
    header = {}
    cookies = {}
    method = ""
    params = ""
    def addheader(self):
        pass
    pass


