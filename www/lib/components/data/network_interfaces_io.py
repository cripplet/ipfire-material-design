from typing import AnyStr

import json

from lib.components import shared
from lib.components.data import shared as shared_data

_NETWORK_DATA_SUBPATH_PATTERN = '/interface/if_octets-'


def get_network_interfaces():
  return [
      i.rsplit('.', 1)[0] for i in
      shared_data.get_logged_members(
          '{root}/{subpath_pattern}'.format(
              root=shared_data.LOG_ROOT_DIRECTORY,
              subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN)
      )
  ]
  

class _NetworkInterfaceIOData(shared_data.MonitoringShim):
  UNIT = 'b'
  def FromEngine(self, interface: AnyStr) -> shared.ConfigType:
    query = [
        'DEF:rx={root}/{subpath_pattern}{interface}.rrd:rx:AVERAGE'.format(
            interface=interface,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN),
        'DEF:tx={root}/{subpath_pattern}{interface}.rrd:tx:AVERAGE'.format(
            interface=interface,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN),
        'XPORT:rx:rx',
        'XPORT:tx:tx',
    ]
    return super(_NetworkInterfaceIOData, self).FromEngine(query=query)


def get_network_interfaces_io_data(interface, step):
  return _NetworkInterfaceIOData().FromEngine(interface=interface)
