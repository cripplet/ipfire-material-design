import json

from lib.components import shared
from lib.components.data import shared as shared_data


class _SwapUsageData(shared_data.MonitoringShim):
  UNIT = 'b'
  def FromEngine(self) -> shared.ConfigType:
    query = sum([
        [
            'DEF:{metric}={root}/swap/swap-{metric}.rrd:value:AVERAGE'.format(
                metric=metric,
                root=shared_data.LOG_ROOT_DIRECTORY),
            'XPORT:{metric}:{metric}'.format(metric=metric),
        ] for metric in ['used', 'free', 'cached']
    ], [])
    return super(_SwapUsageData, self).FromEngine(query=query)


def get_swap_usage_data(step):
  return _SwapUsageData().FromEngine()
