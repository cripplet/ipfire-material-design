ipfire-material-design
----

## Installation

1. Start `app.py` upon startup

## IPFire Layout

* `/var/ipfire/${COMPONENT}/` contains general introspective Perl scripts
* `/srv/web/ipfire/cgi-bin/` contains frontend / rendering code

## Debugging

1. Check `/var/log/httpd/error_log`
1. Check `/var/ipfire/general-functions.pl`
1. Run `perl /srv/web/ipfire/cgi-bin/index.cgi`
