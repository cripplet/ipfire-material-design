import collections

from lib.handlers import settings_handler
from lib.handlers import status_handler

_Route = collections.namedtuple('Route', [
    'rule', 'endpoint', 'view_func', 'provide_automatic_options', 'options'])


def _CreateRoute(
    rule,
    endpoint=None,
    view_func=None,
    provide_automatic_options=None,
    **options):
  return _Route(
    rule=rule,
    endpoint=endpoint,
    view_func=view_func,
    provide_automatic_options=None,
    options=options)._asdict()


ROUTES = [
    _CreateRoute(
        rule='/api/rest/settings/<path:path>',
        endpoint='settings_with_path',
        view_func=settings_handler.settings_handler,
    ),
    _CreateRoute(
        rule='/api/rest/settings/',
        endpoint='settings_without_path',
        view_func=settings_handler.settings_handler,
        defaults={
            'path': '',
        }
    ),
    _CreateRoute(
        rule='/api/rest/status/<path:path>',
        endpoint='status_with_path',
        view_func=status_handler.status_handler,
    ),
    _CreateRoute(
        rule='/api/rest/status/',
        endpoint='status_without_path',
        view_func=status_handler.status_handler,
        defaults={
            'path': '',
        }
    ),
]
