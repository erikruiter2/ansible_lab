---
vars:
  interface:
    name: "{{ item[0].match[0] | trim }}"
    description: "{{ item[1].match[0] | trim }}"
    vlan: "{% if item[5].match[0] == 'access'%}{{ item[2].match[0] | trim }}{% elif item[5].match[0] == 'trunk' %}{{ item[9].match[0]}}{%endif%}"
    voicevlan: "{{ item[3].match[0] | trim }}"
    nativevlan: "{{ item[4].match[0] | trim }}"
    portmode: "{{ item[5].match[0] | trim }}"
    adminstate: "{% if item[6] == None %}enabled{%else%}disabled{%endif%}"
    poe: "{% if item[7] == None %}{{ true }}{%else%}{{ false }}{%endif%}"
    cdp: "{% if item[8] == None %}{{ true }}{%else%}{{ false }}{%endif%}"
    trunkallowedvlan: "{% if item[9].match[0] is iterable and item[9].match[0] is not string%}1{{ item[9].match[0] |join(',')}}{%else%}2{{item[9].match[0]}}{%endif%}"
keys:
  interfaces:
    value: "{{ interface }}"
    start_block: "^interface .+$"
    end_block: "^!$"
    items:
      - "interface (.+)"
      - " description (.+)"
      - " switchport access vlan (.+)"
      - " switchport voice vlan (.+)"
      - " switchport trunk native vlan (.+)"
      - " switchport mode (.+)"
      - " (?P<state>shutdown|no shutdown)" 
      - " (?P<state>power inline auto|power inline never)" 
      - " (?P<state>no cdp enable|cdp enable)"
      - " switchport trunk allowed vlan (.+)" 