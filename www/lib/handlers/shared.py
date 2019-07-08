import http
import json

from lib.handlers import method_not_allowed_handler
from lib.handlers import not_found_handler


def _traverse_dict(d, path):
  d = dict(d)
  if not path:
    return d
  for p in path.split('/'):
    d = d[p]
  return d


def config_handler(path, config, handler):
  if handler.command == 'GET':
    try:
      return handler.respond(
          http.HTTPStatus.OK,
          {'Content-type': 'text/plain'},
          json.dumps(_traverse_dict(config, path), indent=4))
    except KeyError:
      return not_found_handler.not_found_handler(handler)
  return method_not_allowed_handler.method_not_allowed_handler(handler)
