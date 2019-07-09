from lib.components.data import ram_usage
from lib.handlers import shared


def ram_usage_handler():
  return shared.json_handler(
      ram_usage.get_ram_usage_data(step=30))
