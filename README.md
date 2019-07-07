ipfire-material-design
----

## Installation

1. Add `vhost.conf` to `/etc/httpd/conf/vhosts.d/`
1. Add relevant port (`Listen 8080`) to `/etc/httpd/conf/listen.conf`
1. Restart Apache `sudo /etc/init.d/apache restart`

## Debugging

1. Check `/var/log/httpd/error_log`
2. Check `/var/ipfire/general-functions.pl`
3. Run `perl /srv/web/ipfire/cgi-bin/index.cgi`
