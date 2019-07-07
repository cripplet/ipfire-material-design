import httplib


def not_found_handler(handler):
  return handler.respond(
      httplib.NOT_FOUND,
      {'Content-type': 'text/plain'},
      '')
