from lib.components.data import swap_usage
from lib.handlers import shared


def swap_usage_handler(path):
  return shared.config_handler(
      path,
      swap_usage.GetSwapUsageData(step=30))
