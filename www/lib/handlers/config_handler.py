import flask

from lib.components import shared
from lib.components.config import fire_info_config
from lib.components.config import modem_config
from lib.components.config import simple_ipfire_config
from lib.components.config import sys_config

from lib.components.status import connection_status
from lib.components.status import lease_status
from lib.components.status import remote_status
from lib.components.status import vulnerability_status

from lib.handlers import not_found_handler
from lib.handlers import shared as shared_handler


def config_list_components_handler() -> flask.Response:
  return shared_handler.json_handler([c.value for c in shared.Component])


def config_get_handler(component: str) -> flask.Response:
  if component == shared.Component.SYS.value:
    return shared_handler.json_handler(sys_config.get_sys_config())
  if component == shared.Component.FIREINFO.value:
    return shared_handler.json_handler(fire_info_config.get_fire_info_config())
  if component == shared.Component.MODEM.value:
    return shared_handler.json_handler(modem_config.get_modem_config())

  try:
    return shared_handler.json_handler(
        simple_ipfire_config.get_simple_ipfire_config(component))
  except KeyError:
    return not_found_handler.not_found_handler()


def status_get_handler(component: str) -> flask.Response:
  dispatcher = {
    shared.Component.REMOTE.value: remote_status.get_remote_status,
    shared.Component.VULNERABILITY.value: vulnerability_status.get_vulnerability_status,
    shared.Component.CONNECTIONS.value: connection_status.get_connection_status,
    shared.Component.DHCP.value: lease_status.get_lease_status,
  }
  if component in dispatcher:
    return shared_handler.json_handler(dispatcher[component]())
  return not_found_handler.not_found_handler()
