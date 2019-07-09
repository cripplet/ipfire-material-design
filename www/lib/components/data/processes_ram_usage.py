import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def GetProcessesRAMUsageData(step):
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  command = shared_data.GetRRDCommandArgs(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:{process}={root}//collectd/localhost/processes-{process}/ps_rss.rrd:value:AVERAGE'.format(
              process=p,
              root=root),
          'XPORT:{process}:{process}'.format(process=p),
      ] for p in shared_data.GetLoggedProcesses()
  ], [])
  return json.loads(
    shared.GetSysOutput(' '.join(command))
  )
