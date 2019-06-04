# cisco_validate
Ansible role which generates a validation report containing the results of a config check which compares the live config of the interfaces of the switch, with the intented configuration. 

Role description
-----------------------
The role makes use of running config and interface facts gathered by [Napalm](https://napalm-automation.net/) using the napalm_get_facts role.<br> 
The facts are used to generate a text file per device containining any found issues comparing the live and intended configuration.<br>
The role makes use of the [validation_report.j2](../roles/cisco_validate/templates/validation_report.j2) which is populated by the results of a parse_cli filter called: [interface_config.spec](../roles/cisco_validate/tasks/interface_config.spec), which reads the config of the individual interfaces and abstracts the results to match the definitions as mentioned in the hostvars and portprofiles for the device.<br> 
It also checks if the interfaces which should be up, are actually up, and the ones that are configured as down are actually down.<br> 
<br>
This role is currently only supported for Cisco IOL devices using 'Ethernet' naming of their interfaces.<br>

Example
-------
there is a switch called s12-iol.
It has some  interfaces configured as follows in the hostvars file:
```
  Ethernet1/0:
    portprofile: office
  Ethernet1/1:
    portprofile: office
  Ethernet1/2:
    portprofile: office
```
we can change the variables to for instance:
```
  Ethernet1/0:
    portprofile: wifi_accesspoint
  Ethernet1/1:
    portprofile: office
    description: my desktop
  Ethernet1/2:
    portprofile: disabled
```
Eample run:<br>
We can run the provisioning playbook using only the validation tag to avoid configuring the switch and only running the validation.<br>

```~/ansible_lab$ ansible-playbook cisco_provisioning.yml --limit s12-iol --tags validate

PLAY [Device and service provisioning for cisco devices] **********************************************************

TASK [cisco_validate : get config info from device] ***************************************************************
ok: [s12-iol]

TASK [cisco_validate : parse received config info] ****************************************************************
ok: [s12-iol]

TASK [cisco_validate : Write validation report to file] ***********************************************************
ok: [s12-iol]

PLAY RECAP ********************************************************************************************************
s12-iol                    : ok=3    changed=0    unreachable=0    failed=0
```

This will produce a report called: `s12-iol_validation_report.txt`.<BR>
<br>
The file will contain all detected mismatches:
```:~/ansible_lab$ cat s12-iol_validation_report.txt
Validation Report for s12-iol:

Interface configuration issues:
Ethernet1/0 has a mismatch for nativevlan - intended: '998'  actual: ''
Ethernet1/0 has a mismatch for description - intended: 'port configuration for WIFI accesspoints'  actual: 'port configuration for Office desktops and phones'
Ethernet1/0 has a mismatch for portmode - intended: 'trunk'  actual: 'access'
Ethernet1/0 has a mismatch for vlan - intended: '998,999'  actual: '15'
Ethernet1/0 has a mismatch for voicevlan - intended: ''  actual: '39'
Ethernet1/1 has a mismatch for description - intended: 'my desktop'  actual: 'port configuration for Office desktops and phones'
Ethernet1/2 has a mismatch for adminstate - intended: 'disabled'  actual: 'enabled'
Ethernet1/2 has a mismatch for description - intended: 'disabled'  actual: 'port configuration for Office desktops and phones'
Ethernet1/2 has a mismatch for vlan - intended: '2'  actual: '15'
Ethernet1/2 has a mismatch for voicevlan - intended: ''  actual: '39'
Ethernet1/2 has a mismatch for cdp - intended: 'True'  actual: 'False'
interface Ethernet1/2 is up, but should be admin disabled
```
