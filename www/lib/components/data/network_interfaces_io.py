import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


_NETWORK_DATA_SUBPATH_PATTERN = 'collectd/localhost/interface/if_octets-'


def GetNetworkInterfaces():
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  return [
      i.split('.')[0] for i in
      shared_data.GetLoggedMembers(
          '{root}/{subpath_pattern}'.format(
              root=root,
              subpath_pattern=_NETWORK_DATA_SUBPATH_PATTERN)
      )
  ]
  

def GetNetworkInterfacesIOData(interface, step):
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  command = shared_data.GetRRDCommandArgs(
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
    shared.GetSysOutput(' '.join(command))
  )
