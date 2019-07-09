import http
import json

from lib.components.data import ram_usage
from lib.handlers import shared


def ram_usage_handler(path):
  return shared.config_handler(
      path,
      ram_usage.GetRAMUsageData(step=30))
