import collections

from lib.handlers import cpu_frequency_handler
from lib.handlers import network_interfaces_io_handler
from lib.handlers import processes_cpu_time_handler
from lib.handlers import processes_ram_usage_handler
from lib.handlers import ram_usage_handler
from lib.handlers import settings_handler
from lib.handlers import status_handler
from lib.handlers import swap_usage_handler

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
        rule='/api/rest/data/networks/interfaces/<path:path>',
        endpoint='api.rest.data.networks.interfaces.path',
        view_func=network_interfaces_io_handler.network_interfaces_list_handler,
    ),
    _create_route(
        rule='/api/rest/data/networks/interfaces/',
        endpoint='api.rest.data.networks.interfaces',
        view_func=network_interfaces_io_handler.network_interfaces_list_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/networks/io/<string:interface>/<path:path>',
        endpoint='api.rest.data.networks.io.interface.path',
        view_func=network_interfaces_io_handler.network_interfaces_io_handler,
    ),
    _create_route(
        rule='/api/rest/data/networks/io/<string:interface>/',
        endpoint='api.rest.data.networks.io.interface',
        view_func=network_interfaces_io_handler.network_interfaces_io_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/processes/ram/usage/<path:path>',
        endpoint='api.rest.data.processes.ram.usage.path',
        view_func=processes_ram_usage_handler.processes_ram_usage_handler,
    ),
    _create_route(
        rule='/api/rest/data/processes/ram/usage/',
        endpoint='api.rest.data.processes.ram.usage',
        view_func=processes_ram_usage_handler.processes_ram_usage_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/processes/cpu/time/<path:path>',
        endpoint='api.rest.data.processes.cpu.time.path',
        view_func=processes_cpu_time_handler.processes_cpu_time_handler,
    ),
    _create_route(
        rule='/api/rest/data/processes/cpu/time/',
        endpoint='api.rest.data.processes.cpu.time',
        view_func=processes_cpu_time_handler.processes_cpu_time_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/swap/usage/<path:path>',
        endpoint='api.rest.data.swap.usage.path',
        view_func=swap_usage_handler.swap_usage_handler,
    ),
    _create_route(
        rule='/api/rest/data/swap/usage/',
        endpoint='api.rest.data.swap.usage',
        view_func=swap_usage_handler.swap_usage_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/ram/usage/<path:path>',
        endpoint='api.rest.data.ram.usage.path',
        view_func=ram_usage_handler.ram_usage_handler,
    ),
    _create_route(
        rule='/api/rest/data/ram/usage/',
        endpoint='api.rest.data.ram.usage',
        view_func=ram_usage_handler.ram_usage_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/data/cpu/frequency/<path:path>',
        endpoint='api.rest.data.cpu.frequency.path',
        view_func=cpu_frequency_handler.cpu_frequency_handler,
    ),
    _create_route(
        rule='/api/rest/data/cpu/frequency/',
        endpoint='api.rest.data.cpu.frequency',
        view_func=cpu_frequency_handler.cpu_frequency_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/settings/<path:path>',
        endpoint='api.rest.settings.path',
        view_func=settings_handler.settings_handler,
    ),
    _create_route(
        rule='/api/rest/settings/',
        endpoint='api.rest.settings',
        view_func=settings_handler.settings_handler,
        defaults={'path': ''},
    ),
    _create_route(
        rule='/api/rest/status/<path:path>',
        endpoint='api.rest.status.path',
        view_func=status_handler.status_handler,
    ),
    _create_route(
        rule='/api/rest/status/',
        endpoint='api.rest.status',
        view_func=status_handler.status_handler,
        defaults={'path': ''},
    ),
]
