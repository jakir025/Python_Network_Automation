import json
from napalm import get_network_driver

driver = get_network_driver('ios')
device = driver('192.168.184.141', 'jakir', 'Hoss1234')
device.open()

print('###\nGET FACTS\n###')
facts = device.get_facts()
print(json.dumps(facts, sort_keys=True, indent=4))

print('###\nGET ARP\n###')
arptable = device.get_arp_table()
print(json.dumps(arptable, sort_keys=True, indent=4))

print('###\nGET CONFIG\n###')
config = device.get_config()
print(json.dumps(config, sort_keys=True, indent=4))

print('###\nGET INTERFACES\n###')
interfaces = device.get_interfaces()
print(json.dumps(interfaces, sort_keys=True, indent=4))

print('###\nGET INTERFACE COUNTERS\n###')
interfacecounter = device.get_interfaces_counters()
print(json.dumps(interfacecounter, sort_keys=True, indent=4))

print('###\nPING\n###')
pingtest = device.ping('192.168.184.141')
print(json.dumps(pingtest, sort_keys=True, indent=4))

print('###\nTRACEROUTE\n###')
tracetest = device.traceroute('192.168.184.142')
print(json.dumps(tracetest, sort_keys=True, indent=4))

device.close()
