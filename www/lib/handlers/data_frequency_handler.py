import http
import json

from lib.components.data import cpufreq
from lib.handlers import shared


def data_frequency_handler(path):
  return shared.config_handler(
      path,
      cpufreq.GetCPUFrequencyData(step=30))
