import collections
import json

from lib.components import shared
from lib.components.config import shared as shared_config


_SSHConfig = collections.namedtuple('SSHConfig', [
    'enable_ssh_keys',
    'enable_ssh_passwords',
    'enable_ssh_portfw',
    'enable_ssh',
    'ssh_port',
    'enable_agent_forwarding',  
])


class _SSHConfigShim(shared_config.IPFireConfigShim):
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    config = super(_SSHConfigShim, self).FromEngine(data)
    return _SSHConfig(
        enable_ssh_keys=config.get('enable_ssh_keys', True),
        enable_ssh_passwords=config.get('enable_ssh_passwords', True),
        enable_agent_forwarding=config.get('enable_agent_forwarding', False),
        enable_ssh_portfw=config['enable_ssh_portfw'],
        enable_ssh=config['enable_ssh'],
        ssh_port=config['ssh_port'],
    )._asdict()


def get_remote_config() -> shared.ConfigType:
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/remote/settings'.format(ipfire_root=ipfire_root)) as fp:
    return _SSHConfigShim().FromEngine(fp.read())
