# cisco_lldp_topo
Ansible role which generates a lldp_topo.png image containing the discovered network topology of all hosts selected in the playbook. 

Role description
-----------------------
The role makes use of LLDP neighbor facts gathered by [Napalm](https://napalm-automation.net/) using the napalm_get_facts role. The facts are used to generate a [Graphviz](https://www.graphviz.org/) .dot file using a .j2 template.<br>
The template keeps track of already processed interfaces, so that there are no double connections in the graphs.<br>
The output of the template is used as stdin for executing the dot command which generates the image of the topology.
The topology contains all participating hosts along with their connected interfaces.<br>

This role is currently only supported for Cisco IOL devices using 'Ethernet' naming of their interfaces.

Output example
--------------------
```
$ ansible-playbook cisco_lldp_topo.yml

PLAY [Generate LLDP topology playbook] **************************************************

TASK [cisco_lldp_topo : get LLDP information from device] *******************************
ok: [s14-iol]
ok: [s13-iol]
ok: [s11-iol]
ok: [s15-iol]
ok: [s12-iol]
ok: [mgmt-iol]

TASK [cisco_lldp_topo : generate .dot data] *********************************************
ok: [s11-iol -> 127.0.0.1]

TASK [cisco_lldp_topo : generate lldp_topo.png] *****************************************
changed: [s11-iol -> 127.0.0.1]

PLAY RECAP ******************************************************************************
mgmt-iol                   : ok=1    changed=0    unreachable=0    failed=0
s11-iol                    : ok=3    changed=1    unreachable=0    failed=0
s12-iol                    : ok=1    changed=0    unreachable=0    failed=0
s13-iol                    : ok=1    changed=0    unreachable=0    failed=0
s14-iol                    : ok=1    changed=0    unreachable=0    failed=0
s15-iol                    : ok=1    changed=0    unreachable=0    failed=0
```

This generates the following .dot structure:

```
digraph G {
    splines=true;
    rankdir="LR";
    overlap=scalexy;

    edge [
        arrowhead="none"
    ];

    node  [style="rounded,filled,bold", shape=box, width=1.3, fontname="Arial"];
    edge [fontsize=10];
    "s14-iol.inxn.net" -> "mgmt-iol.inxn.net" [minlen=2 headlabel="Et1/0" taillabel="Et1/3"];
    "s11-iol.inxn.net" -> "mgmt-iol.inxn.net" [minlen=2 headlabel="Et0/1" taillabel="Et1/3"];
    "s13-iol.inxn.net" -> "mgmt-iol.inxn.net" [minlen=2 headlabel="Et0/3" taillabel="Et1/3"];
    "mgmt-iol.inxn.net" -> "s15-iol.inxn.net" [minlen=2 headlabel="Et1/3" taillabel="Et1/2"];
    "mgmt-iol.inxn.net" -> "s12-iol.inxn.net" [minlen=2 headlabel="Et1/3" taillabel="Et0/2"];
}
```
And this results in the following image:

<img src='https://github.com/erikruiter2/ansible_lab/raw/master/doc/lldp_topo.png' width=600>

Please note:
It is difficult to align grahpviz elements. Especially in larger topologies the result might look a bit messy.
