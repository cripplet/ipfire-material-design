import http
import json

from lib.components import ipfire_config
from lib.handlers import not_found_handler
from lib.handlers import method_not_allowed_handler


def component_list_handler(handler, component):
  if handler.command == 'GET':
    content = ipfire_config.GetIPFireConfig(component)
    if content:
      return handler.respond(
          http.HTTPStatus.OK,
          {'Content-type': 'text/plain'},
          json.dumps(content, indent=4))
    return not_found_handler.not_found_handler(handler)
  return method_not_allowed_handler.method_not_allowed_handler(handler)
