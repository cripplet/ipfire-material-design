import json

from lib.components import shared
from lib.components.data import shared as shared_data

_NETWORK_PING_SUBPATH_PATTERN = 'ping/ping-'
_NETWORK_DROP_SUBPATH_PATTERN = 'ping/ping_droprate-'


def get_hostnames():
  return [
      i.rsplit('.', 1)[0] for i in
      shared_data.get_logged_members(
          '{root}/{subpath_pattern}'.format(
              root=shared_data.LOG_ROOT_DIRECTORY,
              subpath_pattern=_NETWORK_PING_SUBPATH_PATTERN)
      )
  ]
  

class _NetworkLatencyData(shared_data.MonitoringShim):
  UNIT = 's'
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    command = ' '.join(shared_data.get_rrd_command_args() + [
        'DEF:rtt_ms={root}/{subpath_pattern}{hostname}.rrd:ping:AVERAGE'.format(
            hostname=data,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_PING_SUBPATH_PATTERN),
        'CDEF:rtt=rtt_ms,1000,/',
        'XPORT:rtt:rtt',
    ])
    return super(_NetworkLatencyData, self).FromEngine(data=command)


class _NetworkDropRateData(shared_data.MonitoringShim):
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    command = ' '.join(shared_data.get_rrd_command_args() + [
        'DEF:drop_rate={root}/{subpath_pattern}{hostname}.rrd:value:AVERAGE'.format(
            hostname=data,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_DROP_SUBPATH_PATTERN),
        'XPORT:drop_rate:drop_rate',
    ])
    return super(_NetworkDropRateData, self).FromEngine(data=command)


def get_network_latency_data(hostname, step):
  return _NetworkLatencyData().FromEngine(hostname)


def get_network_drop_rate_data(hostname, step):
  return _NetworkDropRateData().FromEngine(hostname)
