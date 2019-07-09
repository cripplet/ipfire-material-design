import json

from lib.components import ipfire_config
from lib.components import shared
from lib.components.data import shared as shared_data


def GetProcessesCPUTimeData(step):
  root = ipfire_config.GetIPFireConfig()['main']['rrdlog']
  subpath_pattern = 'collectd/localhost/processes-'

  processes = shared_data.GetLoggedMembers(
      '{root}/{subpath_pattern}'.format(
          root=root,
          subpath_pattern=subpath_pattern)
  )

  command = shared_data.GetRRDCommandArgs(
      start_time=step * 20,
      step=step
  ) + sum([
      [
          'DEF:{process}_user={root}/{subpath_pattern}{process}/ps_cputime.rrd:user:AVERAGE'.format(
              process=p,
              root=root,
              subpath_pattern=subpath_pattern),
          'DEF:{process}_system={root}/{subpath_pattern}{process}/ps_cputime.rrd:syst:AVERAGE'.format(
              process=p,
              root=root,
              subpath_pattern=subpath_pattern),
          # returned value in seconds
          'CDEF:{process}={process}_user,{process}_system,+,1000000,/'.format(
              process=p),
          'XPORT:{process}:{process}'.format(process=p),
      ] for p in processes
  ], [])
  return json.loads(
    shared.GetSysOutput(' '.join(command))
  )
