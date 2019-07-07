ipfire-material-design
----

## Installation

1. Clone directory into `/srv/web/ipfire/html/themes/${THEME_NAME}`
1. Change the `THEME` directive in `/var/ipfire/main/settings` to `${THEME_NAME}`

## Debugging

1. Check `/var/log/httpd/error_log`
2. Check `/var/ipfire/general-functions.pl`
3. Run `perl /srv/web/ipfire/cgi-bin/index.cgi`
