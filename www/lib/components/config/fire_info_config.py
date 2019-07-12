import json

from lib.components import shared


class _FireInfoConfig(shared.ShimObject):
  """Read-only IPFire reporting info."""
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    with open('/var/ipfire/fireinfo/profile') as fp:
      return json.loads(fp.read())


def get_fire_info_config() -> shared.ConfigType:
  return _FireInfoConfig().FromEngine(data='')
