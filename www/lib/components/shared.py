import os


class Component(object):
  DDNS = 'ddns'
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


def GetSysOutput(cmd):
  with os.popen(cmd, 'r') as fp:
    return fp.read().strip()
