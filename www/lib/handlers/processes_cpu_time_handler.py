from lib.components.data import processes_cpu_time
from lib.handlers import shared


def processes_cpu_time_handler():
  return shared.json_handler(
      processes_cpu_time.get_processes_cpu_time_data(step=30))
