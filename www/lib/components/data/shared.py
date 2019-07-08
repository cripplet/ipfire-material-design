from lib.components import shared


def GetCoreCount():
  return int(shared.GetSysOutput('cat /proc/cpuinfo | grep processor | wc -l'))
