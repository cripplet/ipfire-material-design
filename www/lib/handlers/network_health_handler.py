from lib.components.data import network_health
from lib.handlers import shared
from lib.handlers import not_found_handler


def network_health_list_handler(path):
  return shared.config_handler(
      path,
      network_health.get_hostnames())


def network_health_latency_handler(hostname, path):
  if hostname not in network_health.get_hostnames():
    return not_found_handler.not_found_handler()

  return shared.config_handler(
      path,
      network_health.get_network_latency_data(
          hostname=hostname,
          step=30))


def network_health_drop_rate_handler(hostname, path):
  if hostname not in network_health.get_hostnames():
    return not_found_handler.not_found_handler()

  return shared.config_handler(
      path,
      network_health.get_network_drop_rate_data(
          hostname=hostname,
          step=30))
