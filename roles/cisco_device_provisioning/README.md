Device provisioning
-------------------

Devices provisioning is done with a jinja template that configures basic device settings based on variables per Ansible group.
Generic variables applicable to all groups can be placed in the ansible_lab/group_vars/all/vars file. 


Implemented variables:
<table>
<th>Variable name</th><th>Example</th><th>Description</th>
<tr><td>snmp<td><pre>snmp:
  - server: 192.168.44.1
    community: public
    version: 2c
</pre><td>SNMP servers and communities</tr>

<tr><td>syslog<td><pre>syslog:
  - server: 192.168.1.1
</pre><td>Syslog servers</tr>

<tr><td>snmp<td><pre>dnsdomain: inxn.net
</pre><td>DNS domain name</tr>

<tr><td>dnsservers<td><pre>dnsservers:
  - 8.8.8.8
  - 4.4.4.4
</pre><td>DNS lookup servers</tr>

<tr><td>ntp<td><pre>ntp:
  - server: 192.168.1.1
</pre><td>NTP servers</tr>

<tr><td>sw_mgmt_svi<td><pre>sw_mgmt_svi:
 - vlan: 10
 - ip: "{{ ansible_host_ip }}"
 - netmask: 255.255.255.0
 - default_gw: 10.1.100.1
</pre><td>SVI for switch management</tr>

<tr><td>users<td><pre>users:
  - name: ansible
    password: "{{ ansible_ssh_pass }}"
  - name: netuser
    password: bladiebla
</pre><td>Device user authentication</tr>

<tr><td>console_password<td><pre>
console_password: "{{ vault_cisco_console_pass }}"
</pre><td>Serial console password</tr>

<tr><td>enable_secret<td><pre>enable_secret: "{{ vault_cisco_enable_secret }}"
</pre><td>Cisco enable secret</tr>

<tr><td>tacacs<td><pre>tacacs:
  - server: 192.168.1.1
    key: "{{ vault_cisco_tacacs_key }}"
  - server: 192.168.1.2
    key: "{{ vault_cisco_tacacs_key }}"
</pre><td>Tacacs authentication settings</tr>

</table>
