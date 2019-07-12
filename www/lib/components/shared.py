import enum
import os

from typing import Dict


class Component(enum.Enum):
  DDNS = 'ddns'
  DHCP = 'dhcp'
  ETHERNET = 'ethernet'
  FIREWALL = 'firewall'
  MAIN = 'main'
  MODEM = 'modem'
  PPP = 'ppp'
  PROXY = 'proxy'
  REMOTE = 'remote'
  VPN = 'vpn'
  SYS = 'sys'
  FIREINFO = 'fireinfo'
  VULNERABILITY = 'vulnerability'
  CONNECTIONS = 'connections'


class ShimObject(object):
  def FromEngine(self, data: str) -> Dict:
    raise NotImplementedError

  def ToEngineFormat(self, data: Dict) -> str:
    raise NotImplementedError


def get_sys_output(cmd: str) -> str:
  with os.popen(cmd, 'r') as fp:
    return fp.read().strip()
