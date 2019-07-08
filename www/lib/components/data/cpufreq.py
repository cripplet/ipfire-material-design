import json

from lib.components import shared
from lib.components.data import shared as shared_data


def GetCPUFrequencyData(step):
  command = [
      'rrdtool',
      'xport',
      '--start=-{start_time}'.format(start_time=step * 20),
      '--json',
      '--showtime',
      '--step={step}'.format(step=step),
  ] + sum([
      [
          'DEF:cpu{core}=/var/log/rrd/collectd/localhost/cpufreq/cpufreq-{core}.rrd:value:AVERAGE'.format(core=i),
          'XPORT:cpu{core}:cpu{core}'.format(core=i),
      ] for i in range(shared_data.GetCoreCount())
  ], [])
  return json.loads(
    shared.GetSysOutput(' '.join(command))
  )
