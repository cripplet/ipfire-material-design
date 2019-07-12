import json
from typing import Dict

from lib.components import shared


class _FireInfoConfig(shared.ShimObject):
  """Read-only IPFire reporting info."""
  def FromEngine(self, data: str) -> Dict:
    with open('/var/ipfire/fireinfo/profile') as fp:
      return json.loads(fp.read())


def get_fire_info_config() -> Dict:
  return _FireInfoConfig().FromEngine(data='')
