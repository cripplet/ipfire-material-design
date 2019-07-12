import json

from lib.components import shared


def _write_ipfire_hash(fn, config):
  """Writes config dict into K=V format."""
  with open(fn, 'w') as fp:
    fp.write('\n'.join(
      [
          '{key}={value}'.format(
              key=k.upper(), value=v
          ) for (k, v) in config.iteritems()]
    ))
    

def _read_ipfire_hash(fn):
  """Parses a K=V file and returns associated dict.

  IPFire uses K=V files as canonical configurations.

  Args:
    fn: Full path to the hash file.

  Returns:
    {k: v} configuration dict.
  """
  with open(fn) as fp:
    parts = [l.strip().split('=', 1) for l in fp.readlines()]
    return {
      k.lower(): v for (k, v) in parts
    }


def _get_system_config():
  return {
      'ipfire': shared.get_sys_output('cat /etc/system-release'),
      'kernel': shared.get_sys_output('uname -a'),
      'pakfire': shared.get_sys_output(
          'cat /opt/pakfire/etc/pakfire.conf | '
          'grep "version =" | cut -d\\" -f2'),
  }


def _get_fire_info_config():
  return json.loads(shared.get_sys_output('cat /var/ipfire/fireinfo/profile'))
  

def get_ipfire_config():
  static_components = set(c.value for c in [
     shared.Component.DDNS,
     shared.Component.DHCP,
     shared.Component.ETHERNET,
     shared.Component.FIREWALL,
     shared.Component.MAIN,
     shared.Component.MODEM,
     shared.Component.PPP,
     shared.Component.PROXY,
     shared.Component.REMOTE,
     shared.Component.VPN,
  ])

  with open('config/ipfire_shim.json') as fp:
    ipfire_shim = json.loads(fp.read())

  config = {
      c: _read_ipfire_hash(
          '{ipfire_root}/{component}/settings'.format(
              ipfire_root=ipfire_shim['ipfire_root'],
              component=c)) for c in static_components
  }

  config.update({
      shared.Component.SYS.value: _get_system_config(),
      shared.Component.FIREINFO.value: _get_fire_info_config(),
  })

  return config
