import collections
import json
import re

from lib.components import shared
from lib.components.config import shared as shared_config


_InterfaceConfig = collections.namedtuple('InterfaceConfig', [
  'enable',
  'enablebootp',
  'start_addr',
  'end_addr',
  'domain_name',
  'default_lease_time',
  'max_lease_time',
  'wins1',
  'wins2',
  'dns1',
  'dns2',
  'ntp1',
  'ntp2',
  'next',
  'file',
  'dns_update_key_name',
  'dns_update_key_secret',
  'dns_update_key_algo',
])

_DHCPConfig = collections.namedtuple('DHCPConfig', [
  'interfaces',
  'sort_leaselist',
  'dns_update_enabled',
  'sort_fleaselist',
])

class _DHCPConfigShim(shared_config.IPFireConfigShim):
  """Formatted DHCP config object.

  TODO(cripplet): Add ADVOPT support.
  """
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    base_config = super(_DHCPConfigShim, self).FromEngine(data=data)
    interfaces = set(['blue', 'green'])
    dhcp_config = {
    }
    interfaces_config = {
        i: {} for i in interfaces
    }
    for (k, v) in base_config.items():
      if k in _DHCPConfig._fields:
        dhcp_config[k] = v
      else:
        interface_property_match = re.match(
            r'(?P<property>[\w_]+)_(?P<interface>{interfaces_regex})'.format(
                interfaces_regex='|'.join(interfaces)
            ),
            k).groupdict()
        interfaces_config[
            interface_property_match['interface']
        ][interface_property_match['property']] = v

    # Validate settings format.
    return _DHCPConfig(
        interfaces={
            i: _InterfaceConfig(
              **c
            )._asdict() for (i, c) in interfaces_config.items()
        },
        **dhcp_config,
    )._asdict()


def get_dhcp_config() -> shared.ConfigType:
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  with open(
      '{ipfire_root}/dhcp/settings'.format(ipfire_root=ipfire_root)) as fp:
    return _DHCPConfigShim().FromEngine(fp.read())
