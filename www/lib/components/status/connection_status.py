import collections
import enum
import re
import socket

from lib.components import shared

_ConnectionStatus = collections.namedtuple('ConnectionStatus', [
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


class _ConnectionShim(shared.ShimObject):
  L4_PROTOCOL_NAME_LOOKUP = {
      int(protocol_number): protocol_name[8:].upper()
      for (protocol_name, protocol_number) in vars(socket).items()
      if protocol_name.startswith('IPPROTO')
  }
  L3_PROTOCOL_NAME_LOOKUP = {
      'IPV6': 'IPv6',
      'IPV4': 'IPv4',
  }

  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    conn_entry_parts = data.split()

    (l3_protocol_name, _, _, l4_protocol_number, ttl) = conn_entry_parts[0:5]

    l3_protocol_name = self.L3_PROTOCOL_NAME_LOOKUP.get(
        l3_protocol_name.upper(),
        l3_protocol_name.upper()
    )

    l4_protocol_name = self.L4_PROTOCOL_NAME_LOOKUP.get(
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


class _ConnectionStatusShim(shared.ShimObject):
  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    return [
        _ConnectionShim().FromEngine(data=l) for l in data.split('\n') if l
    ]


def get_connection_status() -> shared.ConfigType:
  return [
      _ConnectionStatusShim().FromEngine(
          shared.get_sys_output('/usr/local/bin/getconntracktable'))]
