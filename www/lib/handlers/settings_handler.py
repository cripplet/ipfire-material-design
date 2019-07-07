import http
import json

from lib.components import ipfire_config
from lib.handlers import not_found_handler
from lib.handlers import method_not_allowed_handler


def settings_handler(handler, component, property):
  if handler.command == 'GET':
    config = ipfire_config.GetIPFireConfig()
    content = None
    if not component:
      content = config
    elif (
        component and
        component in config and
        property and
        property in config[component]):
      content = config[component][property]
    elif component and component in config and not property:
      content = config[component]
    if content is not None:
      return handler.respond(
          http.HTTPStatus.OK,
          {'Content-type': 'text/plain'},
          json.dumps(content, indent=4))
    return not_found_handler.not_found_handler(handler)
  return method_not_allowed_handler.method_not_allowed_handler(handler)
