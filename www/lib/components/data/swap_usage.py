import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def get_swap_usage_data(step):
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  command = shared_data.get_rrd_command_args(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:{metric}={root}/collectd/localhost/swap/swap-{metric}.rrd:value:AVERAGE'.format(
              metric=metric,
              root=root),
          'XPORT:{metric}:{metric}'.format(metric=metric),
      ] for metric in ['used', 'free', 'cached']
  ], [])
  return json.loads(
    shared.get_sys_output(' '.join(command))
  )
