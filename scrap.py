#!/usr/bin/env python3

import requests
from lxml import html
import re

# Configuration
url = "https://192.168.10.1/status_dhcp_leases.php"  # pfSense machine address
user = 'admin'  # Username for pfSense login
password = 'password'  # Password for pfSense login

def scrape_pfsense_dhcp_ips(url, user, password):
    # Session to maintain cookies
    s = requests.session()
    # Suppressing SSL certificate verification warning
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Initial GET request to get CSRF token
    r = s.get(url, verify=False)
    csrf_token_search = re.search('csrfMagicToken = "(.*)";var', r.text)
    if not csrf_token_search:
        print("CSRF token not found")
        return [], []

    # Login payload
    payload = {
        '__csrf_magic': csrf_token_search.group(1),
        'login': 'Login',
        'usernamefld': user,
        'passwordfld': password
    }

    # POST request for login
    s.post(url, data=payload, verify=False)

    # GET request after login
    r = s.get(url, verify=False)

    # Parsing HTML content
    tree = html.fromstring(r.content)
    # Extracting IP addresses. Assuming the IP addresses are in the second column.
    ip_addresses = tree.xpath('//table[contains(@class, "table")]//tr/td[2]/text()')

    # Extracting DHCP lease information
    lease_info = []
    rows = tree.xpath('//table[contains(@class, "table-striped")]/tbody/tr')
    for row in rows:
        try:
            interface = row.xpath('./td[1]/text()')[0]
            pool_start = row.xpath('./td[2]/text()')[0]
            pool_end = row.xpath('./td[3]/text()')[0]
            used = row.xpath('./td[4]/text()')[0]
            capacity = row.xpath('./td[5]/text()')[0]
            utilization = row.xpath('./td[6]/span/text()')[0]

            lease_info.append({
                'interface': interface,
                'pool_start': pool_start,
                'pool_end': pool_end,
                'used': used,
                'capacity': capacity,
                'utilization': utilization
            })
        except IndexError:
            # Incomplete lease information, skip the row silently
            pass

    return ip_addresses, lease_info

if __name__ == "__main__":
    ip_addresses, lease_info = scrape_pfsense_dhcp_ips(url, user, password)

    # Output data for Zabbix
    print("dhcp.leases.ip_addresses {}".format(",".join(ip_addresses)))
    for lease in lease_info:
        interface = lease['interface']
        print("dhcp.leases.pool_start[{}] {}".format(interface, lease['pool_start']))
        print("dhcp.leases.pool_end[{}] {}".format(interface, lease['pool_end']))
        print("dhcp.leases.used[{}] {}".format(interface, lease['used']))
        print("dhcp.leases.capacity[{}] {}".format(interface, lease['capacity']))
        print("dhcp.leases.utilization.in.percent[{}] {}".format(interface, lease['utilization'].split('%')[0]))
        print()