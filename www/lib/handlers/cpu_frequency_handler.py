import http
import json

from lib.components.data import cpu_frequency
from lib.handlers import shared


def cpu_frequency_handler(path):
  return shared.config_handler(
      path,
      cpu_frequency.GetCPUFrequencyData(step=30))
