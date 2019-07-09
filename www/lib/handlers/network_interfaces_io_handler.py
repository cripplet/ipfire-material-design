from lib.components.data import network_interfaces_io
from lib.handlers import shared
from lib.handlers import not_found_handler


def network_interfaces_list_handler():
  return shared.json_handler(
      network_interfaces_io.get_network_interfaces())


def network_interfaces_io_handler(interface):
  if interface not in network_interfaces_io.get_network_interfaces():
    return not_found_handler.not_found_handler()

  return shared.json_handler(
      network_interfaces_io.get_network_interfaces_io_data(
          interface=interface,
          step=30))
