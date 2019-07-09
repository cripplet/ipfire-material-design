import re

from lib.components import ipfire_config
from lib.components import shared


def GetRRDCommandArgs(start_time, step):
  return [
      'rrdtool',
      'xport',
      '--start=-{start_time}'.format(start_time=start_time),
      '--json',
      '--showtime',
      '--step={step}'.format(step=step),
  ]


def GetCoreCount():
  return int(shared.GetSysOutput('cat /proc/cpuinfo | grep processor | wc -l'))


def GetLoggedMembers(path_pattern):
  return [
      re.match(
          '^{path_pattern}(?P<member>)$'.format(path_pattern=path_pattern),
          d
      ).groupdict()['member'] for d in shared.GetSysOutput(
          'ls -dA {path_pattern}*'.format(
          path_pattern=path_pattern)
      ).split('\n')
  ]
