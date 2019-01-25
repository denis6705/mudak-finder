import telnetlib
from time import sleep
import json
import re
from pprint import pprint as pp

hosts = json.load(open("hosts.json", encoding="utf-8"))

#host = "172.16.0.1"
#user = "root"
#password = "T$2z-artek"
"""
tn = telnetlib.Telnet("172.16.0.1")
tn.write(b"root\n")
sleep(0.2)
tn.write(b"T$2z-artek\n")
sleep(0.2)
tn.write(b"display mac-address 908d-7897-65c3\n")
sleep(0.2)
#tn.write(b"show mac address-table address 24:bc:f8:62:90:30\n")
sleep(1)
s = str(tn.read_very_eager())
pp(s)
match1 = re.search(r'displayed = 0',str(s))
match2 = re.search(r'Eth-Trunk2', str(s))
print(bool(match1))
print(bool(match2))
"""
def convert_mac(m):
    if m[4] == '-':
        return m[0:2] + ":" + m[2:4] + ":" + m[5:7] + ":" + m[7:9] + ":" + m[10:12] + ":" + m[12:14]
    elif m[2] == ':':
        return m[0:2] + m[3:5] + '-' + m[6:8] + m[9:11] + '-' + m[12:14] + m[15:17]

def mudak_tut(host,mac):
    name = host["name"]
    device_type = host["device_type"]
    ip = host["ip"]

    tn = telnetlib.Telnet(ip)
    
    if device_type == "huawei":
        if mac[4] == '-':
            pass
        else:
            mac = convert_mac(mac)
        tn.write(b"root\n")
        sleep(0.2)
        tn.write(b"T$2z-artek\n")
        sleep(0.2)
        tn.write(b"display mac-address " + mac.encode('ascii') + b"\n")
        sleep(2)
        s = str(tn.read_very_eager())
        match1 = re.search(r'displayed = 0',str(s))
        match2 = re.search(r'{}'.format(host['uplink']), str(s))
        if match1: return False
        elif match2: return True
        else: return False
    else:
        if mac[2] == ':':
            pass
        else:
            mac = convert_mac(mac)
        tn.write(b"T$2z-artek\n")
        sleep(0.2)
        tn.write(b"show mac address-table address " + mac.encode('ascii') + b"\n")
        sleep(0.2)
        sleep(2)
        s = str(tn.read_very_eager())
        match1 = re.search(r'dynamic',str(s))
        match2 = re.search(r'{}'.format(host['uplink']), str(s))
        if match1 and (not match2): return True
        else: return False

def naiti_ego(hosts, mac):
    for host in hosts:
        print("Proverka " + host["name"], end='')
        if mudak_tut(host, mac):
            print("   !!! Mudak " + mac + " tut: " + host["name"])
            break
        print('      --     OK')
    return

naiti_ego(hosts, '74d0-2b2c-b2be')
