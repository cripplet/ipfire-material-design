#! /usr/bin/python3

import functools
import json
import re
from http import server

from lib.handlers import settings_handler
from lib.handlers import status_handler
from lib.handlers import method_not_allowed_handler
from lib.handlers import not_found_handler
 

ROUTES = [
    (
        r'^/api/rest/settings$',
        functools.partial(settings_handler.settings_handler, **{'path': ''})),
    (
        r'^/api/rest/status$',
        functools.partial(status_handler.status_handler, **{'path': ''})),
    (
        r'^/api/rest/settings/(?P<path>(\w+/?)*)/?$',
        settings_handler.settings_handler),
    (
        r'^/api/rest/status/(?P<path>(\w+/?)*)/?$',
        status_handler.status_handler),
    (r'.*', not_found_handler.not_found_handler),
]


class Router(server.BaseHTTPRequestHandler):
  def respond(self, resp_code, headers, content):
    self.send_response(resp_code)
    for (k, v) in headers.items():
      self.send_header(k, v)
    self.end_headers()
    self.wfile.write(bytes(content, 'utf-8'))

  def _route(self):
    for (r, h) in ROUTES:
      m = re.match(r, self.path)
      if m is not None:
        return h(
            **m.groupdict(),
            handler=self)

  def do_DELETE(self):
    return self._route()

  def do_GET(self):
    return self._route()

  def do_HEAD(self):
    return self._route()

  def do_PATCH(self):
    return self._route()

  def do_POST(self):
    return self._route()

  def do_PUT(self):
    return self._route()


def main():
  with open('config/debug.json') as fp:
    debug_config = json.loads(fp.read())

  httpd = server.HTTPServer(('', 8080), Router)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.server_close()


if __name__ == '__main__':
  main()
