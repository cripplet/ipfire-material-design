import httplib


def method_not_allowed_handler(handler):
    return handler.respond(
        httplib.METHOD_NOT_ALLOWED,
        {'Content-type': 'text/plain'},
        '')

