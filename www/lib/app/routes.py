import collections

from lib.handlers import config_handler
from lib.handlers import cpu_frequency_handler
from lib.handlers import network_health_handler
from lib.handlers import network_interfaces_io_handler
from lib.handlers import ram_usage_handler
from lib.handlers import swap_usage_handler
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
    _create_route(
        rule='/api/rest/data/network/health/',
        endpoint='api.rest.data.network.health',
        view_func=network_health_handler.network_health_list_handler,
    ),
    _create_route(
        rule='/api/rest/data/network/health/<string:hostname>/latency/',
        endpoint='api.rest.data.network.health.hostnames.latency',
        view_func=network_health_handler.network_health_latency_handler,
    ),
    _create_route(
        rule='/api/rest/data/network/health/<string:hostname>/drop_rate/',
        endpoint='api.rest.data.network.health.hostnames.drop_rate',
        view_func=network_health_handler.network_health_drop_rate_handler,
    ),
    _create_route(
        rule='/api/rest/data/network/io/',
        endpoint='api.rest.data.network.io',
        view_func=network_interfaces_io_handler.network_interfaces_list_handler,
    ),
    _create_route(
        rule='/api/rest/data/network/io/<string:interface>/',
        endpoint='api.rest.data.network.io.interface',
        view_func=network_interfaces_io_handler.network_interfaces_io_handler,
    ),
    _create_route(
        rule='/api/rest/data/swap/usage/',
        endpoint='api.rest.data.swap.usage',
        view_func=swap_usage_handler.swap_usage_handler,
    ),
    _create_route(
        rule='/api/rest/data/ram/usage/',
        endpoint='api.rest.data.ram.usage',
        view_func=ram_usage_handler.ram_usage_handler,
    ),
    _create_route(
        rule='/api/rest/data/cpu/usage/',
        endpoint='api.rest.data.cpu.usage',
        view_func=cpu_frequency_handler.cpu_frequency_handler,
    ),

    _create_route(
        rule='/api/rest/version/',
        endpoint='api.rest.version',
        view_func=version_handler.version_handler,
    ),
    _create_route(
        rule='/api/rest/component/<string:component>/config/',
        endpoint='api.rest.component.component.config.get',
        view_func=config_handler.config_get_handler,
    ),
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
