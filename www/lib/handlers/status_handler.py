from lib.components import statuses
from lib.handlers import shared


def status_handler():
  return shared.json_handler(statuses.get_statuses())
