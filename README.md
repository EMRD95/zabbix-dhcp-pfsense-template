# zabbix-dhcp-pfsense-template
Zabbix template to monitor DHCP lease of Pfsense

As pfSense doesn't show DHCP lease infos in snmp, use of a python script to scrap the web ui + zabbix template with trigger.

Tested on pfSense 2.7.2 and Zabbix 6.4.12

Works with multiple interfaces. Manually adding triggers for the chosen interface is necessary (just clone "Utilization in percent OPT2 RAW" and change the post processing values).

/usr/lib/zabbix/externalscripts/scrap.py

![image](https://github.com/EMRD95/zabbix-dhcp-pfsense-template/assets/114953576/c160e44a-776b-47eb-9502-477d5f9f0c41)

![image](https://github.com/EMRD95/zabbix-dhcp-pfsense-template/assets/114953576/bf413dc5-def8-4646-a0b2-48382e16aa06)

To modify trigger value
![image](https://github.com/EMRD95/zabbix-dhcp-pfsense-template/assets/114953576/67f08f15-e382-48eb-8c61-b54b7128e56b)
