import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def GetRAMUsageData(step):
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  command = shared_data.GetRRDCommandArgs(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:{metric}={root}/collectd/localhost/memory/memory-{metric}.rrd:value:AVERAGE'.format(
              metric=metric,
              root=root),
          'XPORT:{metric}:{metric}'.format(metric=metric),
      ] for metric in ['used', 'free', 'buffered', 'cached']
  ], [])
  return json.loads(
    shared.GetSysOutput(' '.join(command))
  )

