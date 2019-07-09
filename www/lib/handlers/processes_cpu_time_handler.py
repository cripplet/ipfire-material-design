from lib.components.data import processes_cpu_time
from lib.handlers import shared


def processes_cpu_time_handler(path):
  return shared.config_handler(
      path,
      processes_cpu_time.GetProcessesCPUTimeData(step=30))
