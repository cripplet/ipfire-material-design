from lib.components.data import processes_ram_usage
from lib.handlers import shared


def processes_ram_usage_handler():
  return shared.json_handler(
      processes_ram_usage.get_processes_ram_usage_data(step=30))
