import httplib
import json

from lib import ipfire_config
from lib.handlers import method_not_allowed_handler


def simple_handler(handler):
  if handler.command == 'GET':
    return handler.respond(
        httplib.OK,
        {'Content-type': 'text/plain'},
        json.dumps(ipfire_config.GetIPFireConfig(), indent=4))
  return method_not_allowed_handler.method_not_allowed_handler(handler)
