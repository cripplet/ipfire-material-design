import flask

from lib.components import shared
from lib.components.config import dhcp_config
from lib.components.config import fire_info_config
from lib.components.config import modem_config
from lib.components.config import remote_config
from lib.components.config import simple_ipfire_config
from lib.components.config import sys_config

from lib.components.status import connection_status
from lib.components.status import firewall_status
from lib.components.status import lease_status
from lib.components.status import remote_status
from lib.components.status import vulnerability_status

from lib.handlers import not_found_handler
from lib.handlers import shared as shared_handler


def config_list_components_handler() -> flask.Response:
  return shared_handler.json_handler([c.value for c in shared.Component])


def config_get_handler(component: str) -> flask.Response:
  dispatcher = {
    shared.Component.SYS.value: sys_config.get_sys_config,
    shared.Component.FIREINFO.value: fire_info_config.get_fire_info_config,
    shared.Component.MODEM.value: modem_config.get_modem_config,
    shared.Component.REMOTE.value: remote_config.get_remote_config,
    shared.Component.DHCP.value: dhcp_config.get_dhcp_config,
  }
  if component in dispatcher:
    return shared_handler.json_handler(dispatcher[component]())

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
    shared.Component.FIREWALL.value: firewall_status.get_firewall_status,
  }
  if component in dispatcher:
    return shared_handler.json_handler(dispatcher[component]())
  return not_found_handler.not_found_handler()
