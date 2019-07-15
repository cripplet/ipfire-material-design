import json

from lib.components import shared
from lib.components.config import shared as shared_config


class _DHCPConfigShim(shared_config.IPFireConfigShim):
  pass


def get_dhcp_config() -> shared.ConfigType:
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/dhcp/settings'.format(ipfire_root=ipfire_root)) as fp:
    return _DHCPConfigShim().FromEngine(fp.read())
