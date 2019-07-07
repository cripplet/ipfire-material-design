from lib.components import ipfire_config
from lib.handlers import shared


def settings_handler(path, handler):
  return shared.config_handler(path, ipfire_config.GetIPFireConfig(), handler)
