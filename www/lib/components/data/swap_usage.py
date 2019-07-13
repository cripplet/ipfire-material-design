import json

from lib.components import shared
from lib.components.data import shared as shared_data


class _SwapUsageData(shared_data.MonitoringShim):
  UNIT = 'b'
  def FromEngine(self) -> shared.ConfigType:
    command = ' '.join(shared_data.get_rrd_command_args() + sum([
        [
            'DEF:{metric}={root}/swap/swap-{metric}.rrd:value:AVERAGE'.format(
                metric=metric,
                root=shared_data.LOG_ROOT_DIRECTORY),
            'XPORT:{metric}:{metric}'.format(metric=metric),
        ] for metric in ['used', 'free', 'cached']
    ], []))
    return super(_SwapUsageData, self).FromEngine(data=command)


def get_swap_usage_data(step):
  return _SwapUsageData().FromEngine()
