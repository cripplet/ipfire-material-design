from typing import AnyStr

import flask

from lib.components.data import cpu_frequency
from lib.components.data import network_health
from lib.components.data import network_interfaces_io
from lib.components.data import ram_usage
from lib.components.data import swap_usage

from lib.handlers import not_found_handler
from lib.handlers import shared


def network_io_data_list_handler() -> flask.Response:
  return shared.json_handler(
      network_interfaces_io.get_network_interfaces())


def network_io_data_get_handler(interface: AnyStr) -> flask.Response:
  try:
    return shared.json_handler(
        network_interfaces_io.get_network_interfaces_io_data(
            interface=interface))
  except KeyError:
    return not_found_handler.not_found_handler()


def network_health_data_list_handler() -> flask.Response:
  return shared.json_handler(
      network_health.get_hostnames())


def network_health_data_get_handler(hostname: AnyStr, metric: AnyStr) -> flask.Response:
  dispatcher = {
    'latency': network_health.get_network_latency_data,
    'drop_rate': network_health.get_network_drop_rate_data,
  }
  if metric in dispatcher:
    try:
      return shared.json_handler(
          dispatcher[metric](hostname=hostname))
    except KeyError:
      return not_found_handler.not_found_handler()
  return not_found_handler.not_found_handler()


def simple_data_get_handler(component: AnyStr) -> flask.Response:
  dispatcher = {
    'cpu': cpu_frequency.get_cpu_frequency_data,
    'ram': ram_usage.get_ram_usage_data,
    'swap': swap_usage.get_swap_usage_data,
  }

  if component in dispatcher:
    return shared.json_handler(dispatcher[component]())

  return not_found_handler.not_found_handler()
