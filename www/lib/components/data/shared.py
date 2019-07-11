import re

from lib.components import ipfire_config
from lib.components import shared


def get_rrd_command_args(start_time, step):
  return [
      'rrdtool',
      'xport',
      '--start=-{start_time}'.format(start_time=start_time),
      '--json',
      '--step={step}'.format(step=step),
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
