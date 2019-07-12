import json
import os
from typing import AnyStr

from lib.components import shared
from lib.components.config import shared as shared_config


def get_simple_ipfire_config(component: AnyStr) -> shared.ConfigType:
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']
  fn = '{ipfire_root}/{component}/settings'.format(
      ipfire_root=ipfire_root,
      component=component)

  if component not in set(
      [c.value for c in shared.Component]) or not os.path.exists(fn):
    raise KeyError(
        'Cannot find specified component \'{c}\''.format(
            c=component))

  with open(fn) as fp:
    return shared_config.IPFireConfigShim().FromEngine(fp.read())
