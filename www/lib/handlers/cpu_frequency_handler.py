from lib.components.data import cpu_frequency
from lib.handlers import shared


def cpu_frequency_handler():
  return shared.json_handler(
      cpu_frequency.get_cpu_frequency_data(step=30))
