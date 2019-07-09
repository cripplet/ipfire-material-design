from lib.components import shared


def GetRRDCommandArgs(start_time, step):
  return [
      'rrdtool',
      'xport',
      '--start=-{start_time}'.format(start_time=start_time),
      '--json',
      '--showtime',
      '--step={step}'.format(step=step),
  ]

def GetCoreCount():
  return int(shared.GetSysOutput('cat /proc/cpuinfo | grep processor | wc -l'))
