import http


def method_not_allowed_handler(handler):
    return handler.respond(
        http.HTTPStatus.METHOD_NOT_ALLOWED,
        {'Content-type': 'text/plain'},
        '')

