import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


_NETWORK_PING_SUBPATH_PATTERN = 'collectd/localhost/ping/ping-'
_NETWORK_DROP_SUBPATH_PATTERN = 'collectd/localhost/ping/ping_droprate-'


def get_hostnames():
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  return [
      i.rsplit('.', 1)[0] for i in
      shared_data.get_logged_members(
          '{root}/{subpath_pattern}'.format(
              root=root,
              subpath_pattern=_NETWORK_PING_SUBPATH_PATTERN)
      )
  ]
  

def get_network_latency_data(hostname, step):
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  command = shared_data.get_rrd_command_args(
      start_time=step * 20,
      step=step
  ) + [
      'DEF:rtt_ms={root}/{subpath_pattern}{hostname}.rrd:ping:AVERAGE'.format(
          hostname=hostname,
          root=root,
          subpath_pattern=_NETWORK_PING_SUBPATH_PATTERN),
      'CDEF:rtt=rtt_ms,1000,/',
      'XPORT:rtt:rtt',
  ]
  return json.loads(
    shared.get_sys_output(' '.join(command))
  )


def get_network_drop_rate_data(hostname, step):
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  command = shared_data.get_rrd_command_args(
      start_time=step * 20,
      step=step
  ) + [
      'DEF:drop_rate={root}/{subpath_pattern}{hostname}.rrd:value:AVERAGE'.format(
          hostname=hostname,
          root=root,
          subpath_pattern=_NETWORK_DROP_SUBPATH_PATTERN),
      'XPORT:drop_rate:drop_rate',
  ]
  return json.loads(
    shared.get_sys_output(' '.join(command))
  )
