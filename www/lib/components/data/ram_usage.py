import json

from lib.components import shared
from lib.components.data import shared as shared_data


class _RAMUsageData(shared_data.MonitoringShim):
  UNIT = 'b'
  def FromEngine(self) -> shared.ConfigType:
    data = ' '.join(
        shared_data.get_rrd_command_args() + sum([
            [
                'DEF:{metric}={root}/memory/memory-{metric}.rrd:value:AVERAGE'.format(
                    metric=metric,
                    root=shared_data.LOG_ROOT_DIRECTORY),
                'XPORT:{metric}:{metric}'.format(metric=metric),
            ] for metric in ['used', 'free', 'buffered', 'cached']
        ], []))

    return super(_RAMUsageData, self).FromEngine(data=data)


def get_ram_usage_data(step):
  return _RAMUsageData().FromEngine()
