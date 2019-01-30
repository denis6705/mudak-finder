import telnetlib
from time import sleep
import json
import re
from pprint import pprint as pp

hosts = json.load(open("hosts.json", encoding="utf-8"))


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
        if not match1 and not match2:
            print()
            print(re.sub(r'\s+', ' | ',s.split('\\r\\n')[-5]))
            return True
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
        if match1 and (not match2):
            print()
            print(re.sub(r'\s+', ' | ',s.split('\\r\\n')[10]))
            return True
        else: return False

def naiti_ego(hosts, mac):
    for host in hosts:
        print("Proverka " + host["name"], end='')
        if mudak_tut(host, mac):
            pass
        print("")
    return

try:
    naiti_ego(hosts, '7c:b0:c2:83:0e:e6')
except:
    pass
