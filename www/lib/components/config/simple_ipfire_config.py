import json
from typing import Dict

from lib.components import shared
from lib.components.config import shared as shared_config


def get_simple_ipfire_config(component: str) -> Dict:
  if component not in set([c.value for c in shared.Component]):
    raise KeyError(
        'Cannot find specified component \'{c}\''.format(
            c=component))

  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/{component}/settings'.format(
          ipfire_root=ipfire_root,
          component=component)) as fp:
    return shared_config.IPFireConfigShim().FromEngine(fp.read())
