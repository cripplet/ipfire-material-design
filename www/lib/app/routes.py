import collections

from lib.handlers import config_handler
from lib.handlers import data_handler
from lib.handlers import version_handler

_Route = collections.namedtuple('Route', [
    'rule', 'endpoint', 'view_func', 'provide_automatic_options', 'options'])


def _create_route(
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
    # network health data
    _create_route(
        rule='/api/rest/data/health/<string:hostname>/<string:metric>/',
        endpoint='api.rest.data.health.hostname.metric',
        view_func=data_handler.network_health_data_get_handler,
    ),
    _create_route(
        rule='/api/rest/data/health/',
        endpoint='api.rest.data.health',
        view_func=data_handler.network_health_data_list_handler,
    ),

    # network IO data
    _create_route(
        rule='/api/rest/data/io/<string:interface>/',
        endpoint='api.rest.data.io.interface',
        view_func=data_handler.network_io_data_get_handler,
    ),
    _create_route(
        rule='/api/rest/data/io/',
        endpoint='api.rest.data.io',
        view_func=data_handler.network_io_data_list_handler,
    ),

    # misc. usage data
    _create_route(
        rule='/api/rest/data/<string:component>/',
        endpoint='api.rest.data.component',
        view_func=data_handler.simple_data_get_handler,
    ),

    # server version data
    _create_route(
        rule='/api/rest/version/',
        endpoint='api.rest.version',
        view_func=version_handler.version_handler,
    ),

    # misc. system configs
    _create_route(
        rule='/api/rest/component/<string:component>/config/',
        endpoint='api.rest.component.component.config.get',
        view_func=config_handler.config_get_handler,
    ),

    # misc. system statuses
    _create_route(
        rule='/api/rest/component/<string:component>/status/',
        endpoint='api.rest.component.component.status.get',
        view_func=config_handler.status_get_handler,
    ),

    _create_route(
        rule='/api/rest/component/',
        endpoint='api.rest.component.get',
        view_func=config_handler.config_list_components_handler,
    ),
]
