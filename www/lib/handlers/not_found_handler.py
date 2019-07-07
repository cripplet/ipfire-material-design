import http


def not_found_handler(handler):
  return handler.respond(
      http.HTTPStatus.NOT_FOUND,
      {'Content-type': 'text/plain'},
      '')
