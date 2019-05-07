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
    access: readonly</pre><td>SNMP servers and communities. Access can be readonly/readwrite. When ommited access will be readwrite</tr>
<tr><td>syslog<td><pre>syslog:
  - server: 192.168.1.1</pre><td>Syslog servers</tr>
<tr><td>dnsdomain<td><pre>dnsdomain: inxn.net</pre><td>DNS domain name</tr>
<tr><td>dnsservers<td><pre>dnsservers:
  - 8.8.8.8
  - 4.4.4.4</pre><td>DNS lookup servers</tr>
<tr><td>ntp<td><pre>ntp:
  - server: 192.168.1.1</pre><td>NTP servers</tr>
<tr><td>sw_mgmt_svi<td><pre>sw_mgmt_svi:
 - vlan: 10
   ip: "{{ ansible_host_ip }}"
   netmask: 255.255.255.0
   default_gw: 10.1.100.1</pre><td>SVI for switch management. Generates a vlan interface (SVI) for inband management. It will add a default gateway and set source-interfaces for various protocol. (A bit shaky, since this interface needs to be present any way to access the device in the lab.)</tr>
<tr><td>users<td><pre>users:
  - name: ansible
    password: "{{ ansible_ssh_pass }}"
  - name: netuser
    password: bladiebla</pre><td>Device user authentication</tr>
<tr><td>console_password<td><pre>
console_password: "{{ vault_console_pass }}"</pre><td>Serial console password</tr>
<tr><td>enable_secret<td><pre>enable_secret: "{{ vault_enable_secret }}"</pre><td>Cisco enable secret</tr>
<tr><td>tacacs<td><pre>tacacs:
  - server: 192.168.1.1
    key: "{{ vault_cisco_tacacs_key }}"
  - server: 192.168.1.2
    key: "{{ vault_cisco_tacacs_key }}"</pre><td>Tacacs authentication settings</tr>
</table>

VLAN service provisioning
-------------------------

Each interface on the siwtch provides a vlan service for the connected device.<br>
There are many different device types which can be connected to the switch, which can have different ethernet switching requirements. To group the required statements for configuring a port, a port profile can be created, so that the configuration per port stays compact, without redundant information.

* The port profiles are specified in the group_vars file of the related group.
* Portprofiles are assigned in the hostvars file of the switch. Each interface can list a single portprofile (or none).
* Variables in the portprofile can be overwritten in the hostvars file.

Some practical examples of portprofiles, which are written in the group_vars file:
<table>
  <th>Example</th><th>Comments</th>
  <tr><td><pre>
  - name: cctv
    description: CCTV device
    portmode: access
    vlan: 411
    portsecurity: sticky
    poe: True
    cdp: False</pre></td><td>
    </td></tr><td><pre>
  - name: office
    portmode: access
    vlan: 15
    voicevlan: 39
    poe: True
    cdp: True</pre></td><td>
    </td></tr><td><pre>
  - name: wifi_ap
    description: WIFI Accesspoint
    portmode: trunk
    vlan: 998,999
    nativevlan: 998
    poe: True
    cdp: False</pre></td><td>
    </td></tr><td><pre>
  - name: lab_uplink_port
    description: Uplink port
    portmode: trunk
    vlan: all
    poe: False
    cdp: True</pre></td><td>
    </td></tr>
</table>

The hostvars for the interfaces on a switch can look like following:
```
interfaces:
  Ethernet0/0:
    portprofile: lab_uplink_port
  Ethernet0/1:
    portprofile: cctv
  Ethernet0/2:
    description: Office file server
    portprofile: office
    poe: False
  Ethernet0/3:
    portprofile: office
  Ethernet0/4:
    portprofile: office
  Ethernet0/5:
    description: AP ground floor
    portprofile: wifi_ap
  Ethernet0/6:
    description: AP first floor
    portprofile: wifi_ap
  Ethernet0/7:
    portprofile: disabled
```

This is a list of all variables currently available:

|Name | Possible values | Default | description |
| -- | -- | -- | -- |
|adminstate | enabled / disabled | disabled | Administrative state of the port |
|description | any string | empty | Port description |
|portmode | access / trunk | access | Port tagging |
|vlan | number(1) / range(1,2,3-6) / none / all | required | VLAN is used for both access and trunk ports, can be noted any way that is also used on CLI |
|voicevlan | 1-4095 | no voicevlan | Switchport voice vlan statement |
|nativevlan | 2-4095 | no native vlan(1) | native vlan, only used in conjunction with port mode trunk |
|poe | Yes / True / No / False | No | Enable Power over Ethernet on the port |
|cdp | Yes / True / No / False | Yes | Enable Cisco Discovery Protocol on the Port |
|portsecurity | none / sticky / aaaa.bbbb.cccc | none | Assigns port security to the port. This can be a single sticky address, or a specified MAC address |
|customstatements | any cisco statement | none | Allows a list of custom config statements to add to the port |
  
