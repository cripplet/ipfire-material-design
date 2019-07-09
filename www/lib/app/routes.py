import collections

from lib.handlers import cpu_frequency_handler
from lib.handlers import ram_usage_handler
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
        rule='/api/rest/data/ram/usage/<path:path>',
        endpoint='api.rest.data.ram.usage.path',
        view_func=ram_usage_handler.ram_usage_handler,
    ),
    _CreateRoute(
        rule='/api/rest/data/ram/usage/',
        endpoint='api.rest.data.ram.usage',
        view_func=ram_usage_handler.ram_usage_handler,
        defaults={'path': ''},
    ),
    _CreateRoute(
        rule='/api/rest/data/cpu/frequency/<path:path>',
        endpoint='api.rest.data.cpu.frequency.path',
        view_func=cpu_frequency_handler.cpu_frequency_handler,
    ),
    _CreateRoute(
        rule='/api/rest/data/cpu/frequency/',
        endpoint='api.rest.data.cpu.frequency',
        view_func=cpu_frequency_handler.cpu_frequency_handler,
        defaults={'path': ''},
    ),
    _CreateRoute(
        rule='/api/rest/settings/<path:path>',
        endpoint='api.rest.settings.path',
        view_func=settings_handler.settings_handler,
    ),
    _CreateRoute(
        rule='/api/rest/settings/',
        endpoint='api.rest.settings',
        view_func=settings_handler.settings_handler,
        defaults={'path': ''},
    ),
    _CreateRoute(
        rule='/api/rest/status/<path:path>',
        endpoint='api.rest.status.path',
        view_func=status_handler.status_handler,
    ),
    _CreateRoute(
        rule='/api/rest/status/',
        endpoint='api.rest.status',
        view_func=status_handler.status_handler,
        defaults={'path': ''},
    ),
]
