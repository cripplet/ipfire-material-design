import collections
import json
import re

from lib.components import shared
from lib.components.config import shared as shared_config

# TODO(cripplet): Add more fields here that may or may not matter.
_InterfaceConfig = collections.namedtuple('InterfaceConfig', [
    'dev',
    'mac',
    'description',
    'driver',
    'ip',
    'network_mask',
    'network_ip',
    'broadcast',
])

# TODO(cripplet): Add more fields here.
_EthernetConfig = collections.namedtuple('EthernetConfig', [
    'interfaces',
])

class _EthernetConfigShim(shared_config.IPFireConfigShim):
  INTERFACE_PROPERTY_LOOKUP_TABLE = {
      'macaddr': 'mac',
      'address': 'ip',
      'netmask': 'network_mask',
      'netaddress': 'network_ip',
  }

  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    config = super(_EthernetConfigShim, self).FromEngine(data=data)

    interface_names = set(['red', 'blue', 'green'])

    interfaces = {
      i: {} for i in interface_names
    }

    for (k, v) in config.items():
      property_match = re.match(
          '^(?P<interface>{interface_pattern})_(?P<property>[\w_]+)'.format(
              interface_pattern='|'.join(interface_names),
          ), k)
      if property_match is not None:
        property_match_dict = property_match.groupdict()
        translated_property_name = self.INTERFACE_PROPERTY_LOOKUP_TABLE.get(
            property_match_dict['property'],
            property_match_dict['property'])
        if translated_property_name in _InterfaceConfig._fields:
          interfaces[property_match_dict['interface']][
              translated_property_name] = v

    with open('config/ipfire_shim.json') as fp:
      ipfire_root = json.loads(fp.read())['ipfire_root']

    with open(
        '{ipfire_root}/red/remote-ipaddress'.format(
            ipfire_root=ipfire_root)) as fp:
      interfaces['red']['ip'] = fp.read().strip()

    # Settings validation
    return _EthernetConfig({
        k: _InterfaceConfig(**v)._asdict() for (k, v) in interfaces.items() if v
    })

def get_ethernet_config() -> shared.ConfigType:
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/ethernet/settings'.format(ipfire_root=ipfire_root)) as fp:
    return _EthernetConfigShim().FromEngine(fp.read())
