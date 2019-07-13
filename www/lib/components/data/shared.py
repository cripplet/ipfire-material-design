import json
import re

from lib.components import shared
from lib.components.config import simple_ipfire_config

LOG_ROOT_DIRECTORY = '{rrd_root}/collectd/localhost'.format(
  rrd_root=simple_ipfire_config.get_simple_ipfire_config(
      shared.Component.MAIN.value)['rrdlog']
)


class MonitoringShim(shared.ShimObject):
  UNIT = None
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    rrd_data = json.loads(shared.get_sys_output(data))
    rrd_data['meta']['unit'] = self.UNIT
    del rrd_data['about']
    return rrd_data


def get_rrd_command_args():
  return [
      'rrdtool',
      'xport',
      '--start=-600',
      '--json',
      '--step=30',
  ]


def get_core_count():
  return int(shared.get_sys_output('cat /proc/cpuinfo | grep processor | wc -l'))


def get_logged_members(path_pattern):
  return [
      re.match(
          '^{path_pattern}(?P<member>.*)$'.format(path_pattern=path_pattern),
          d
      ).groupdict()['member'] for d in shared.get_sys_output(
          'ls -dA {path_pattern}*'.format(
          path_pattern=path_pattern)
      ).split('\n')
  ]
