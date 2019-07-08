from lib.components import statuses
from lib.handlers import shared


def status_handler(path, handler):
  return shared.config_handler(path, statuses.GetStatuses(), handler)
