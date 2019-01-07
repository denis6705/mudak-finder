import telnetlib
import time
import json
import re

hosts = json.load(open("hosts.json", encoding="utf-8"))

#host = "172.16.0.1"
#user = "root"
#password = "T$2z-artek"
"""
tn = telnetlib.Telnet("172.16.13.199")
#tn.write(b"root\n")
tn.write(b"T$2z-artek\n")
#tn.write(b"display mac-address 0427-581f-6022\n")
tn.write(b"show mac address-table address 24:bc:f8:62:93:30\n")
time.sleep(1)
s = str(tn.read_very_eager())
print(s)
match = re.search(r'displayed = 0',str(s))
print(bool(match))
"""
def convert_mac(m):
    if m[4] == '-':
        return m[0:2] + ":" + m[2:4] + ":" + m[5:7] + ":" + m[7:9] + ":" + m[10:12] + ":" + m[12:14]
    elif m[2] == ':':
        return m[0:2] + m[3:5] + '-' + m[6:8] + m[9:11] + '-' + m[12:14] + m[15:17]

def mudak_tut(host,mac):
    name = host["name"]
    type = host["type"]
    ip = host["ip"]

    tn = telnetlib.Telnet(ip)
    
    if type == "huawei":
        if mac[4] == '-':
            pass
        else:
            mac = convert_mac(mac)
        tn.write(b"root\n")
        tn.write(b"T$2z-artek\n")
        tn.write(b"display mac-address " + mac.encode('ascii') + b"\n")
        time.sleep(2)
        s = str(tn.read_very_eager())
        match = re.search(r'displayed = 0',str(s))
        if match: return False
        else: return True
    else:
        if mac[2] == ':':
            pass
        else:
            mac = convert_mac(mac)
        tn.write(b"T$2z-artek\n")
        tn.write(b"show mac address-table address " + mac.encode('ascii') + b"\n")
        time.sleep(2)
        s = str(tn.read_very_eager())
        match = re.search(r'dynamic',str(s))
        if match: return True
        else: return False

def naiti_ego(hosts, mac):
    for host in hosts:
        print("Proverka " + host["name"])
        if mudak_tut(host, mac):
            print("Mudak " + mac + " tut: " + host["name"])
            break
    return

naiti_ego(hosts, '74d0-2b2c-b2be')
