import collections
import http

from lib.handlers import not_found_handler
from lib.handlers import method_not_allowed_handler

_ErrorHandler = collections.namedtuple('ErrorHandler', [
    'code_or_exception', 'f'])


def _create_error_handler(code_or_exception, f):
  return _ErrorHandler(
    code_or_exception=code_or_exception,
    f=f)._asdict()


ERROR_HANDLERS = [
    _create_error_handler(
        http.HTTPStatus.NOT_FOUND,
        lambda e: not_found_handler.not_found_handler()),
    _create_error_handler(
        http.HTTPStatus.METHOD_NOT_ALLOWED,
        lambda e: method_not_allowed_handler.method_not_allowed_handler())
]
