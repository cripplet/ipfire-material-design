import collections
import datetime
import os

from lib.components import shared

_SSHKey = collections.namedtuple('SSHKey', ['file', 'type', 'fingerprint', 'size'])
_SSHSession = collections.namedtuple('SSHSession', ['username', 'login_timestamp', 'ip'])


class _RemoteComponentShim(shared.ShimObject):
  def FromEngine(self) -> shared.ConfigType:
    return {
        'keys': [
            _SSHKey(
                file=fn,
                type=type,
                size=int(shared.get_sys_output(
                    '/usr/bin/ssh-keygen -lf {file}  | cut -d" " -f1'.format(
                        file=fn))) / 8,
                fingerprint=shared.get_sys_output(
                    '/usr/bin/ssh-keygen -lf {file}  | cut -d" " -f2'.format(
                        file=fn)),
            )._asdict() for (fn, type) in set([
                ('/etc/ssh/ssh_host_key.pub', 'RSA1'),
                ('/etc/ssh/ssh_host_rsa_key.pub', 'RSA2'),
                ('/etc/ssh/ssh_host_dsa_key.pub', 'DSA'),
                ('/etc/ssh/ssh_host_ecdsa_key.pub', 'ECDSA'),
                ('/etc/ssh/ssh_host_ed25519_key.pub', 'ED25519'),
            ]) if os.path.exists(fn)],
        'sessions': [
            _SSHSession(
                username=username,
                login_timestamp=int(
                    datetime.datetime.timestamp(
                        datetime.datetime.strptime(
                            '{date} {time}'.format(
                                date=date_since,
                                time=time_since),
                            '%Y-%m-%d %H:%M'))),
                ip=ip.strip('()'),
            )._asdict() for (username, _, date_since, time_since, ip) in [
              l.split() for l in shared.get_sys_output('who -s').split('\n')
            ]
        ],
    }



def get_remote_status() -> shared.ConfigType:
  return _RemoteComponentShim().FromEngine()
