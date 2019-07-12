import collections
import json

from lib.components import shared


_FirewallRule = collections.namedtuple('FirewallRule', [
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
    'icmp_target',
    'dest_filter_type',
    'dest_filter',
    'comment',
    'is_logged',
    'is_scheduled',
    'schedule',
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

_IPFireFirewallRule = collections.namedtuple('IPFireFirewallRule', [
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



class _FirewallRuleShim(shared.ShimObject):
  BOOL_TRANSLATE_LOOKUP = {
      'ON': True,
      '': False,
  }

  def FromEngine(self, data: shared.EngineType) -> shared.ConfigType:
    r = _IPFireFirewallRule(*data.split(','))._asdict()
    return _FirewallRule(
        position=int(r['position']),
        action=r['action'],
        chain=r['chain'],
        is_enabled=self.BOOL_TRANSLATE_LOOKUP[r['is_enabled']],
        src_type=r['src_type'],
        src=r['src'],
        dest_type=r['dest_type'],
        dest=r['dest'],
        use_src_filter=self.BOOL_TRANSLATE_LOOKUP[r['use_src_filter']],
        l4_protocol=r['l4_protocol'],
        # TODO(cripplet): Check if this should be a list instead.
        icmp_types=r['icmp_types'],
        src_filter=r['src_filter'],
        is_enabled_srv=self.BOOL_TRANSLATE_LOOKUP[r['is_enabled_srv']],
        icmp_target=r['icmp_target'],
        dest_filter_type=r['dest_filter_type'],
        dest_filter=r['dest_filter'],
        comment=r['comment'],
        is_logged=self.BOOL_TRANSLATE_LOOKUP[r['is_logged']],
        is_scheduled=self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled']],
        schedule={
            'monday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_monday']],
            'tuesday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_tuesday']],
            'wednesday': self.BOOL_TRANSLATE_LOOKUP[
                r['is_scheduled_wednesday']],
            'thursday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_monday']],
            'friday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_friday']],
            'saturday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_saturday']],
            'sunday': self.BOOL_TRANSLATE_LOOKUP[r['is_scheduled_sunday']],
        },
        start_time=r['start_time'],
        end_time=r['end_time'],
        is_enabled_nat=self.BOOL_TRANSLATE_LOOKUP[r['is_enabled_nat']],
        nat_target=r['nat_target'],
        dnat_port=int(r['dnat_port']) if r['dnat_port'] else None,
        nat_target_type=r['nat_target_type'],
        is_connection_pool_throttled=self.BOOL_TRANSLATE_LOOKUP[
            r['is_connection_pool_throttled']],
        connection_pool_size=int(
            r['connection_pool_size']) if r['connection_pool_size'] else 0,
        is_connection_rate_limited=self.BOOL_TRANSLATE_LOOKUP[
            r['is_connection_rate_limited']],
        connection_rate_limit_scalar=int(
            r['connection_rate_limit_scalar']
        ) if r['connection_rate_limit_scalar'] else 0,
        connection_rate_limit_unit=r['connection_rate_limit_unit'],
    )._asdict()


def get_firewall_status() -> shared.ConfigType:
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

  rules = {}

  for (k, fn) in firewall_rules_configs.items():
    with open(fn) as fp:
      rules[k] = [
          _FirewallRuleShim().FromEngine(l.strip()) for l in fp.readlines()
      ]
  return rules
