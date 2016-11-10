check_http_yaml
===============

Nagios/Icinga check plugin to get yaml data via http and check the value of a key-value pair.
Requires the servers response header to have "Content-Type: *yaml*".

EXAMPLE:

python check_http_yaml.py icinga-host.local 9000 /icinga-status?query=STATUSFILEAGETT STATUSFILEAGETT

OK - value: 3|statusfileagett=3
