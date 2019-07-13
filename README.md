# ipfire-rest
Experimental REST API for IPFire

## Installation

1. Install Python[3] `distutils`: `pakfire install python-distutils`
1. Install `pip`: `python3 -m ensurepip --upgrade`
1. Download relevant packages (`requirements.txt`) by installing from source: `sudo python3 setup.py install`
1. Run the Python server: `python3 server.py`

## IPFire Layout

* `/var/ipfire/${COMPONENT}/` contains general introspective Perl scripts
* `/srv/web/ipfire/cgi-bin/` contains frontend / rendering code

## Debugging

1. Check `/var/log/httpd/error_log`
1. Check `/var/ipfire/general-functions.pl`
1. Run `perl /srv/web/ipfire/cgi-bin/index.cgi`
