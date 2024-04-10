# zabbix-dhcp-pfsense-template
Zabbix template to monitor DHCP lease of Pfsense

As pfSense doesn't show DHCP lease infos in snmp, use of a python script to scrap the web ui + zabbix template with trigger.

Tested of pfSense 2.7.2 and Zabbix 6.4.12

Works with multiple interfaces. Manually adding triggers for the chosen interface necessary (just clone OPT2).

/usr/lib/zabbix/externalscripts/scrap.py
