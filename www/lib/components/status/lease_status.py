import collections
import datetime
import json
import re
import os

from lib.components import shared

_FixedLease = collections.namedtuple('FixedLease', [
    'mac',
    'ip',
    'enabled',
    'next_server',
    'filename',
    'root_path',
    'remark',
])

_DynamicLease = collections.namedtuple('DynamicLease', [
    'ip',
    'start',
    'end',
    'hardware_type',
    'mac',
    'hostname',
])


class _FixedLeaseShim(shared.ShimObject):
  BOOL_TRANSLATE_DICT = {
    'on': True,
    'off': False,
  }

  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    lease = _FixedLease(*data.strip().split(','))._asdict()
    lease['enabled'] = self.BOOL_TRANSLATE_DICT[lease['enabled']]
    return lease


class _DynamicLeaseShim(shared.ShimObject):

  LEASE_REGEX = re.compile(
      r'lease (?P<ip>(?:\d+(?:\.|:)?)+) {(?:\n.*)*?'
      r'(?:\s+starts \d+ (?P<start>[\/\d\ \:]+);)(?:\n.*)*?'
      r'(?:\s+ends \d+ (?P<end>[\/\d\ \:]+);)(?:\n.*)*?'
      r'(?:\s+hardware (?P<hardware_type>\w+) (?P<mac>(?:\w+:?)+);)(?:\n.*)*?'
      r'(?:\s+ uid.*)?(?:\n.*)*?'
      r'(?:\s+client-hostname \"(?P<hostname>\S+)\";)?(?:\n.*)*?\n'
      r'}',
      re.MULTILINE)

  HARDWARE_TYPE_LOOKUP = {
      'ethernet': 'ETHERNET',
      'token-ring': 'TOKEN_RING',
  }

  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
      leases = [
          _DynamicLease(**m.groupdict())._asdict() for m in self.LEASE_REGEX.finditer(data)
      ]
      for l in leases:
          l.update({
              'start': int(
                  datetime.datetime.timestamp(
                      datetime.datetime.strptime(l['start'], '%Y/%m/%d %H:%M:%S'))),
              'end': int(
                  datetime.datetime.timestamp(
                      datetime.datetime.strptime(l['end'], '%Y/%m/%d %H:%M:%S'))),
              'hardware_type': self.HARDWARE_TYPE_LOOKUP[l['hardware_type']],
          })

      return leases


class _LeaseStatusShim(shared.ShimObject):
  def FromEngine(self) -> shared.ConfigType:
    with open('config/ipfire_shim.json') as fp:
      ipfire_root = json.loads(fp.read())['ipfire_root']

    fixedleases_fn = '{ipfire_root}/dhcp/fixleases'.format(ipfire_root=ipfire_root)
    if os.path.isfile(fixedleases_fn):
      with open(fixedleases_fn) as fp:
        fixedleases_lines = fp.readlines()
    else:
      fixedleases_lines = []

    with open('/var/state/dhcp/dhcpd.leases') as fp:
      return {
          'fixed': [
              _FixedLeaseShim().FromEngine(data=l) for l in fixedleases_lines],
          'dynamic': _DynamicLeaseShim().FromEngine(data=fp.read()),
      }


def get_lease_status() -> shared.ConfigType:
  return _LeaseStatusShim().FromEngine()
