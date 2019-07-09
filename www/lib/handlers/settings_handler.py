from lib.components import ipfire_config
from lib.handlers import shared


def settings_handler():
  return shared.json_handler(ipfire_config.get_ipfire_config())
