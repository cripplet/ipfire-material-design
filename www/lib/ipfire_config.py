import json


def _WriteIPFireHash(fn, config):
  """Writes config dict into K=V format."""
  with open(fn, 'w') as fp:
    fp.write('\n'.join(
      [
          '{key}={value}'.format(
              key=k, value=v
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
      k: v for (k, v) in parts
    }


def GetIPFireConfig():
  config = {}

  with open('config/ipfire_shim.json') as fp:
    ipfire_shim = json.loads(fp.read())

  for component in (
      'ddns',
      'ethernet',
      'firewall',
      'main',
      'modem',
      'ppp',
      'proxy',
      'remote',
      'vpn'):
    config.update({
        component: {
            'settings': _ReadIPFireHash(
                '{ipfire_root}/{component}/settings'.format(
                    ipfire_root=ipfire_shim['ipfire_root'],
                    component=component)),
        },
    })

  return config
