import json
from typing import Dict

from lib.components.config import shared


class _ModemConfigShim(shared.IPFireConfigShim):
  BOOL_TRANSLATE_DICT = {
      'yes': True,
      'no': False,
  }


def get_modem_config():
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/modem/settings'.format(ipfire_root=ipfire_root)) as fp:
    return _ModemConfigShim().FromEngine(fp.read())
