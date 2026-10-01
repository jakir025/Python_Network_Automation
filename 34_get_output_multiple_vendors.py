import json
from napalm import get_network_driver

cisco = ['192.168.184.141','192.168.184.142']
arista = ['192.168.184.144']

for cisco_ip in cisco:
    print ('Connecting to Cisco device' + str(cisco_ip))
    driver = get_network_driver('ios')
    device = driver(cisco_ip, 'jakir', 'Hoss1234')
    device.open()
    facts = device.get_facts()
#    print(json.dumps(facts, sort_keys=True, indent=4))
    print ('Cisco device' + str(cisco_ip) + 'Software version is ' + facts['os_version'])
    
for arista_ip in arista:
    print ('Connecting to Arista device' + str(arista_ip))
    driver = get_network_driver('eos')
    device = driver(arista_ip, 'jakir', 'Hoss1234')
    device.open()
    facts = device.get_facts()
#    print(json.dumps(facts, sort_keys=True, indent=4))
    print ('Arista device' + str(arista_ip) + 'Software version is ' + facts['os_version'])
    device.close()    
    
    

