import json

from lib.components import shared
from lib.components.data import shared as shared_data


class _RAMUsageData(shared_data.MonitoringShim):
  UNIT = 'b'
  def FromEngine(self) -> shared.ConfigType:
    query = sum([
        [
            'DEF:{metric}={root}/memory/memory-{metric}.rrd:value:AVERAGE'.format(
                metric=metric,
                root=shared_data.LOG_ROOT_DIRECTORY),
            'XPORT:{metric}:{metric}'.format(metric=metric),
        ] for metric in ['used', 'free', 'buffered', 'cached']
    ], [])

    return super(_RAMUsageData, self).FromEngine(query=query)


def get_ram_usage_data(step):
  return _RAMUsageData().FromEngine()
