#! /usr/bin/python


import BaseHTTPServer
import httplib
import json
import re
import SimpleHTTPServer

from lib.handlers import simple_handler
from lib.handlers import not_found_handler
from lib.handlers import method_not_allowed_handler
 

ROUTES = [
    (r'^/$', simple_handler.simple_handler),
    (r'.*', not_found_handler.not_found_handler),
]


class Router(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def respond(self, resp_code, headers, content):
    self.send_response(resp_code)
    for (k, v) in headers.iteritems():
      self.send_header(k, v)
    self.end_headers()
    self.wfile.write(content)

  def _route(self):
    for (r, h) in ROUTES:
      if re.match(r, self.path):
        return h(self)

  def do_GET(self):
    return self._route()

  def do_HEAD(self):
    return self._route()

  def do_POST(self):
    return self._route()

  def do_PUT(self):
    return self._route()

  def do_DELETE(self):
    return self._route()


def main():
  with open('config/debug.json') as fp:
    debug_config = json.loads(fp.read())

  httpd = BaseHTTPServer.HTTPServer(('', 8080), Router)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.server_close()


if __name__ == '__main__':
  main()
