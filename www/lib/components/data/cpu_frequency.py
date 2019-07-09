import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def get_cpu_frequency_data(step):
  root = ipfire_config.get_ipfire_config()['main']['rrdlog']
  command = shared_data.get_rrd_command_args(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:cpu{core}={root}/collectd/localhost/cpufreq/cpufreq-{core}.rrd:value:AVERAGE'.format(
              core=i,
              root=root),
          'XPORT:cpu{core}:cpu{core}'.format(core=i),
      ] for i in range(shared_data.get_core_count())
  ], [])
  return json.loads(
    shared.get_sys_output(' '.join(command))
  )
