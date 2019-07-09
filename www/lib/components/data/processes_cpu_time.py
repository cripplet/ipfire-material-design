import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def GetProcessesCPUTimeData(step):
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  command = shared_data.GetRRDCommandArgs(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:{process}_user={root}//collectd/localhost/processes-{process}/ps_cputime.rrd:user:AVERAGE'.format(
              process=p,
              root=root),
          'DEF:{process}_system={root}//collectd/localhost/processes-{process}/ps_cputime.rrd:syst:AVERAGE'.format(
              process=p,
              root=root),
          # returned value in seconds
          'CDEF:{process}={process}_user,{process}_system,+,1000000,/'.format(
              process=p),
          'XPORT:{process}:{process}'.format(process=p),
      ] for p in shared_data.GetLoggedProcesses()
  ], [])
  return json.loads(
    shared.GetSysOutput(' '.join(command))
  )
