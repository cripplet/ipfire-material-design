import os


class Component(object):
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


def get_sys_output(cmd):
  with os.popen(cmd, 'r') as fp:
    return fp.read().strip()
