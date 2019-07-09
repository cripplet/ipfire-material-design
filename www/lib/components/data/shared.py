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


def GetLoggedProcesses():
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  return [
      re.match(
          '^{root}/collectd/localhost/processes-(?P<process>.*)$'.format(
              root=root), d).groupdict()['process']
      for d in shared.GetSysOutput(
          'ls -dA {root}/collectd/localhost/processes-*'.format(
              root=root)).split('\n')
  ]
