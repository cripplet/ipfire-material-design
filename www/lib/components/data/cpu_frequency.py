import json

from lib.components import shared
from lib.components.data import shared as shared_data


class _CPUFrequencyData(shared_data.MonitoringShim):
  UNIT = 'hz'
  def FromEngine(self) -> shared.ConfigType:
    query = sum([
        [
            'DEF:cpu{core}={root}/cpufreq/cpufreq-{core}.rrd:value:AVERAGE'.format(
                core=i,
                root=shared_data.LOG_ROOT_DIRECTORY),
            'XPORT:cpu{core}:cpu{core}'.format(core=i),
        ] for i in range(shared_data.get_core_count())
    ], [])

    return super(_CPUFrequencyData, self).FromEngine(query=query)


def get_cpu_frequency_data():
  return _CPUFrequencyData().FromEngine()
