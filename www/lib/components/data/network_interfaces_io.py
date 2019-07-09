import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


_NETWORK_DATA_SUBPATH_PATTERN = 'collectd/localhost/interface/if_octets-'


def get_network_interfaces():
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  return [
      i.rsplit('.', 1)[0] for i in
      shared_data.get_logged_members(
          '{root}/{subpath_pattern}'.format(
              root=root,
              subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN)
      )
  ]
  

def get_network_interfaces_io_data(interface, step):
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  command = shared_data.get_rrd_command_args(
      start_time=step * 20,
      step=step
  ) + [
      'DEF:rx={root}/{subpath_pattern}{interface}.rrd:rx:AVERAGE'.format(
          interface=interface,
          root=root,
          subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN),
      'DEF:tx={root}/{subpath_pattern}{interface}.rrd:tx:AVERAGE'.format(
          interface=interface,
          root=root,
          subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN),
      'XPORT:rx:rx',
      'XPORT:tx:tx',
  ]
  return json.loads(
    shared.get_sys_output(' '.join(command))
  )
