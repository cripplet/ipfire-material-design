from collections import namedtuple

import datetime
import os
import re

from lib.components import shared


SSHKey = namedtuple('SSHKey', ['file', 'type', 'fingerprint', 'size'])
SSHSession = namedtuple('SSHSession', ['username', 'active_since', 'ip'])
VulnerabilityLookup = namedtuple('VulnerabilityLookup', [
    'description',
    'cves'])
KnownVulnerability = namedtuple('KnownVulnerability', [
    'name',
    'description',
    'cves',
    'vulnerability_status',
    'vulnerability_description',
])

_VULNERABILITY_STATUS = {
    'Not affected': 'NOT_AFFECTED',
    'Vulnerability: ': 'VULNERABLE',
    'Mitigation: ': 'MITIGATED',
}

_VULNERABILITIES = {
    'l1tf': VulnerabilityLookup(
        description='Foreshadow',
        cves=['CVE-2018-3620'],
    ),
    'mds': VulnerabilityLookup(
        description='Fallout/ZombieLoad/RIDL',
        cves=['CVE-2018-12126', 'CVE-2018-12130', 'CVE-2018-12127', 'CVE-2019-11091']
    ),
    'meltdown': VulnerabilityLookup(
        description='Meltdown',
        cves=['CVE-2017-5754'],
    ),
    'spec_store_bypass': VulnerabilityLookup(
        description='Spectre Variant 4',
        cves=['CVE-2018-3639'],
    ),
    'spectre_v1': VulnerabilityLookup(
        description='Spectre Variant 1',
        cves=['CVE-2017-5753'],
    ),
    'spectre_v2': VulnerabilityLookup(
        description='Spectre Variant 2',
        cves=['CVE-2017-5715'],
    ),
}


def _generate_vulnerabilities():
  c = []
  vuln_dir = '/sys/devices/system/cpu/vulnerabilities/'
  for v in os.listdir(vuln_dir):
    data = shared.get_sys_output(
        'cat {path}'.format(path=os.path.join(vuln_dir, v)))
    m = re.match('^(?P<status>(Not affected|Vulnerable: |Mitigation: ))(?P<description>.*)$', data)
    c.append(KnownVulnerability(
        name=v,
        vulnerability_status=_VULNERABILITY_STATUS[m.groupdict().get('status', '')],
        vulnerability_description=m.groupdict().get('description', ''),
        **_VULNERABILITIES.get(v, VulnerabilityLookup(description='', cves=[]))._asdict()
    )._asdict())
  return c


def _generate_ssh_sessions():
  return [
      SSHSession(
          username=username,
          active_since=str(
              datetime.datetime.strptime(
                  '{date} {time}'.format(date=date_since, time=time_since),
                  '%Y-%m-%d %H:%M')),
          ip=ip.strip('()'),
      )._asdict() for (username, _, date_since, time_since, ip) in [
        l.split() for l in shared.get_sys_output('who -s').split('\n')
      ]
  ]


def _generate_ssh_keys():
  return [
      SSHKey(
          file=fn,
          type=type,
          size=int(shared.get_sys_output(
              '/usr/bin/ssh-keygen -lf {file}  | cut -d" " -f1'.format(
                  file=fn))),
          fingerprint=shared.get_sys_output(
              '/usr/bin/ssh-keygen -lf {file}  | cut -d" " -f2'.format(
                  file=fn)),
      )._asdict() for (fn, type) in set([
          ('/etc/ssh/ssh_host_key.pub', 'RSA1'),
          ('/etc/ssh/ssh_host_rsa_key.pub', 'RSA2'),
          ('/etc/ssh/ssh_host_dsa_key.pub', 'DSA'),
          ('/etc/ssh/ssh_host_ecdsa_key.pub', 'ECDSA'),
          ('/etc/ssh/ssh_host_ed25519_key.pub', 'ED25519'),
      ])
      if os.path.exists(fn)
  ]


def get_statuses():
  return {
    shared.Component.REMOTE: {
        'keys': _generate_ssh_keys(),
        'sessions': _generate_ssh_sessions(),
    },
    shared.Component.VULNERABILITY: _generate_vulnerabilities(),
  }
