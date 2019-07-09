from lib.components.data import network_interfaces_io
from lib.handlers import shared
from lib.handlers import not_found_handler


def network_interfaces_list_handler(path):
  return shared.config_handler(
      path,
      network_interfaces_io.GetNetworkInterfaces())


def network_interfaces_io_handler(interface, path):
  if interface not in network_interfaces_io.GetNetworkInterfaces():
    return not_found_handler.not_found_handler()

  return shared.config_handler(
      path,
      network_interfaces_io.GetNetworkInterfacesIOData(
          interface=interface,
          step=30))
