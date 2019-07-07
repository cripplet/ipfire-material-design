import json

from lib.components import shared


def _WriteIPFireHash(fn, config):
  """Writes config dict into K=V format."""
  with open(fn, 'w') as fp:
    fp.write('\n'.join(
      [
          '{key}={value}'.format(
              key=k.upper(), value=v
          ) for (k, v) in config.iteritems()]
    ))
    

def _ReadIPFireHash(fn):
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


def _GetSystemConfig():
  return {
      'ipfire': shared.GetSysOutput('cat /etc/system-release'),
      'kernel': shared.GetSysOutput('uname -a'),
      'pakfire': shared.GetSysOutput(
          'cat /opt/pakfire/etc/pakfire.conf | '
          'grep "version =" | cut -d\\" -f2'),
  }


def _GetFireInfoConfig():
  return json.loads(shared.GetSysOutput('cat /var/ipfire/fireinfo/profile'))
  

def GetIPFireConfig():
  static_components = set([
     shared.Component.DDNS,
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
      c: _ReadIPFireHash(
          '{ipfire_root}/{component}/settings'.format(
              ipfire_root=ipfire_shim['ipfire_root'],
              component=c)) for c in static_components
  }

  config.update({
      shared.Component.SYS: _GetSystemConfig(),
      shared.Component.FIREINFO: _GetFireInfoConfig(),
  })

  return config
