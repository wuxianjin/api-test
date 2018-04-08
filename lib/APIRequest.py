#!/usr/bin/python
# -*- coding: utf8 -*-

from requests.sessions import HTTPAdapter
import requests
from conf import apiconf
from util import log


class APIRequest:
    LOG_NAME = "request"

    def __init__(self, host, port):

        schem = "https" if apiconf.API_PORT == 443 else "http"

        self.url_host = "%s://%s:%s" % (schem, host, port)

        self.api_session = requests.Session()
        self.api_session.mount("http://", HTTPAdapter(max_retries=0))
        self.api_session.mount("https://", HTTPAdapter(max_retries=0))
        self.errors = {}

    def add_header(self, name, value):

        self.api_session.headers.update({name: value})

    def _timeout(self):

        if requests.__version__ >= "2.9.1":
            return 3, apiconf.REQUEST_TIMEOUT
        else:
            return apiconf.REQUEST_TIMEOUT

    def get(self, url):

        log.getlog(self.LOG_NAME).debug("GET %s" % self.url_host + url)

        resp = self.api_session.get(self.url_host + url, timeout=self._timeout())

        def _read():
            return resp.text

        resp.read = _read
        try:
            resp.raise_for_status()
        except Exception, e:
            print "resp===>\n", resp.read()
            print repr(e)
            raise
        return resp

    def post(self, url, raw_data, stream=False, headers={}):
        log.getlog(self.LOG_NAME).debug("POST %s, raw_data[%s]"
                                        % (self.url_host + url,
                                           raw_data))

        resp = self.api_session.post(self.url_host + url,
                                     # headers=self.headers,
                                     data=raw_data,
                                     stream=stream,
                                     headers=headers,
                                     timeout=self._timeout())

        def _read():
            return resp.text

        resp.read = _read
        try:
            resp.raise_for_status()
        except Exception, e:
            print "resp===>\n", resp.read()
            print repr(e)
            raise
        return resp
