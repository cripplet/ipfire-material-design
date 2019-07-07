import httplib
import json

from lib.components import ipfire_config
from lib.handlers import method_not_allowed_handler


def component_list_handler(handler, component):
  if handler.command == 'GET':
    return handler.respond(
        httplib.OK,
        {'Content-type': 'text/plain'},
        json.dumps(ipfire_config.GetIPFireConfig(component), indent=4))
  return method_not_allowed_handler.method_not_allowed_handler(handler)
