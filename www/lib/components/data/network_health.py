from typing import AnyStr

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
  def FromEngine(self, hostname: AnyStr) -> shared.ConfigType:
    query = [
        'DEF:rtt_ms={root}/{subpath_pattern}{hostname}.rrd:ping:AVERAGE'.format(
            hostname=hostname,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_PING_SUBPATH_PATTERN),
        'CDEF:rtt=rtt_ms,1000,/',
        'XPORT:rtt:rtt',
    ]
    return super(_NetworkLatencyData, self).FromEngine(query=query)


class _NetworkDropRateData(shared_data.MonitoringShim):
  def FromEngine(self, hostname: AnyStr) -> shared.ConfigType:
    query = [
        'DEF:drop_rate={root}/{subpath_pattern}{hostname}.rrd:value:AVERAGE'.format(
            hostname=hostname,
            root=shared_data.LOG_ROOT_DIRECTORY,
            subpath_pattern=_NETWORK_DROP_SUBPATH_PATTERN),
        'XPORT:drop_rate:drop_rate',
    ]
    return super(_NetworkDropRateData, self).FromEngine(query=query)


def get_network_latency_data(hostname):
  if hostname not in set(get_hostnames()):
    raise KeyError(
        'Cannot find specified hostname \'{h}\''.format(
            h=hostname))
  return _NetworkLatencyData().FromEngine(hostname=hostname)


def get_network_drop_rate_data(hostname):
  if hostname not in set(get_hostnames()):
    raise KeyError(
        'Cannot find specified hostname \'{h}\''.format(
            h=hostname))
  return _NetworkDropRateData().FromEngine(hostname=hostname)
