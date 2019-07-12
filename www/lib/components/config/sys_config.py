from typing import Dict

from lib.components import shared
from lib.components.config import shared as shared_config


class _SysConfigShim(shared.ShimObject):
  """Read-only system info."""

  def FromEngine(self, data: str) -> Dict:
    return {
        'ipfire': shared.get_sys_output('cat /etc/system-release'),
        'kernel': shared.get_sys_output('uname -a'),
        'pakfire': shared.get_sys_output(
            'cat /opt/pakfire/etc/pakfire.conf | '
            'grep "version =" | cut -d\\" -f2',
        ),
    }


def get_sys_config() -> Dict:
  return _SysConfigShim().FromEngine(data='')
