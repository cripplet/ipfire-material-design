from collections import namedtuple

import datetime
import json
import os
import re
import socket

from lib.components import shared


_SSHKey = namedtuple('SSHKey', ['file', 'type', 'fingerprint', 'size'])
_SSHSession = namedtuple('SSHSession', ['username', 'active_since', 'ip'])
_ConnectionStatus = namedtuple('ConnectionStatus', [
    'l3_name',
    'l4_name',
    'src_addr',
    'src_port',
    'dest_addr',
    'dest_port',
    'rx',
    'tx',
    'state',
    'ttl',
])
_FixedLease = namedtuple('FixedLease', [
    'mac',
    'ip',
    'enabled',
    'next_server',
    'filename',
    'root_path',
    'remark',
])
_FirewallRule = namedtuple('FirewallRule', [
    'position',
    'action',
    'chain',
    'is_enabled',
    'src_type',
    'src',
    'dest_type',
    'dest',
    'use_src_filter',
    'l4_protocol',
    'icmp_types',
    'src_filter',
    'is_enabled_srv',
    'dest_protocol',  # deprecated
    'icmp_target',
    'dest_filter_type',
    'dest_filter',
    'comment',
    'is_logged',
    'is_scheduled',
    'is_scheduled_monday',
    'is_scheduled_tuesday',
    'is_scheduled_wednesday',
    'is_scheduled_thursday',
    'is_scheduled_friday',
    'is_scheduled_saturday',
    'is_scheduled_sunday',
    'start_time',
    'end_time',
    'is_enabled_nat',
    'nat_target',
    'dnat_port',  # external port
    'nat_target_type',
    'is_connection_pool_throttled',
    'connection_pool_size',
    'is_connection_rate_limited',
    'connection_rate_limit_scalar',
    'connection_rate_limit_unit',
])


def _process_connection(conn_entry):
  l4_protocol_name_lookup = {
      int(protocol_number): protocol_name[8:].upper()
      for (protocol_name, protocol_number) in vars(socket).items()
      if protocol_name.startswith('IPPROTO')
  }

  l3_protocol_name_translate = {
      'IPV6': 'IPv6',
      'IPV4': 'IPv4',
  }

  conn_entry_parts = conn_entry.split()

  (l3_protocol_name, _, _, l4_protocol_number, ttl) = conn_entry_parts[0:5]

  l3_protocol_name = l3_protocol_name_translate.get(
      l3_protocol_name.upper(),
      l3_protocol_name.upper()
  )

  l4_protocol_name = l4_protocol_name_lookup.get(
      int(l4_protocol_number),
      l4_protocol_number).upper()

  src_addr_entries = [
      e.split('=')[-1] for e in conn_entry_parts if e.startswith('src=')]
  src_port_entries = [
      int(e.split('=')[-1]) for e in conn_entry_parts if e.startswith(
          'sport=')]
  dest_addr_entries = [
      e.split('=')[-1] for e in conn_entry_parts if e.startswith('dst=')]
  dest_port_entries = [
      int(e.split('=')[-1]) for e in conn_entry_parts if e.startswith(
          'dport=')]
  (tx, rx) = [
      int(e.split('=')[-1]) for e in conn_entry_parts if e.startswith(
          'bytes=')]

  return _ConnectionStatus(
      l3_name=l3_protocol_name,
      l4_name=l4_protocol_name,
      src_addr=src_addr_entries,
      src_port=src_port_entries,
      dest_addr=dest_addr_entries,
      dest_port=dest_port_entries,
      rx=rx,
      tx=tx,
      state=conn_entry_parts[5].upper() if l4_protocol_name == 'TCP' else '',
      ttl=int(ttl),
  )._asdict()


def _generate_connections():
  return [
      _process_connection(c) for c in shared.get_sys_output(
          '/usr/local/bin/getconntracktable').split('\n') if c]


def _generate_dynamic_leases():
  with open('/var/state/dhcp/dhcpd.leases') as fp:
    content = fp.read()

  p = re.compile(
      r'lease (?P<ip>(?:\d+(?:\.|:)?)+) {(?:\n.*)*?'
      r'(?:\s+starts \d+ (?P<start>[\/\d\ \:]+);)(?:\n.*)*?'
      r'(?:\s+ends \d+ (?P<end>[\/\d\ \:]+);)(?:\n.*)*?'
      r'(?:\s+hardware (?P<hardware_type>\w+) (?P<mac>(?:\w+:?)+;))(?:\n.*)*?'
      r'(?:\s+ uid.*)?(?:\n.*)*?'
      r'(?:\s+client-hostname \"(?P<hostname>\S+)\";)?(?:\n.*)*?\n'
      r'}', re.MULTILINE)

  leases = [
    m.groupdict() for m in p.finditer(content)
  ]
  for l in leases:
    l.update({
        'start': int(
            datetime.datetime.timestamp(
                datetime.datetime.strptime(l['start'], '%Y/%m/%d %H:%M:%S'))),
        'end': int(
            datetime.datetime.timestamp(
                datetime.datetime.strptime(l['end'], '%Y/%m/%d %H:%M:%S'))),
    })
  return leases


def _generate_dhcp_leases():
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  return {
      'fixed': [
          _FixedLease(*l.split(','))._asdict() for l in shared.get_sys_output(
              'cat {ipfire_root}/dns/fixleases'.format(
                  ipfire_root=ipfire_root))
      ],
      'dynamic': _generate_dynamic_leases(),
  }


def _generate_firewall_rules():
  with open('config/ipfire_shim.json') as fp:
    ipfire_root = json.loads(fp.read())['ipfire_root']

  firewall_rules_configs = {
    'forward': '{ipfire_root}/firewall/config'.format(
        ipfire_root=ipfire_root),
    'input': '{ipfire_root}/firewall/input'.format(
        ipfire_root=ipfire_root),
    'output': '{ipfire_root}/firewall/outgoing'.format(
        ipfire_root=ipfire_root),
  }

  firewall_rules = {}
  for (k, f) in firewall_rules_configs.items():
    with open(f) as fp:
      # IPFire replaces commas in the comment string with semi-colons
      firewall_rules[k] = [
          _FirewallRule(
              *l.strip().split(',')
          )._asdict() for l in fp.readlines()
      ]

  return firewall_rules
    

def get_statuses():
  return {
    shared.Component.CONNECTIONS.value: _generate_connections(),
    shared.Component.DHCP.value: _generate_dhcp_leases(),
    shared.Component.FIREWALL.value: _generate_firewall_rules(),
  }
