import enum
import os

from typing import AnyStr, Dict, Union, List


EngineType = AnyStr
ConfigType = Union[Dict, List]


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
  CONNECTIONS = 'connection'


class ShimObject(object):
  def FromEngine(self, data: EngineType) -> ConfigType:
    raise NotImplementedError

  def ToEngineFormat(self, data: ConfigType) -> EngineType:
    raise NotImplementedError


def get_sys_output(cmd: str) -> str:
  with os.popen(cmd, 'r') as fp:
    return fp.read().strip()
