import json
from napalm import get_network_driver

cisco = ['192.168.184.141','192.168.184.142']
arista = ['192.168.184.144']

def getfacts(ips,vendor,mode):
    for ip in ips:
        print ('Connecting to '+ vendor + str(ip))
        driver = get_network_driver(mode)
        device = driver(ip, 'jakir', 'Hoss1234')
        device.open()
        facts = device.get_facts()
#       print(json.dumps(facts, sort_keys=True, indent=4))
        print (vendor+ 'Device' + str(ip) + ' Software version is ' + facts['os_version'])
        device.close()
        
getfacts(cisco,'cisco ','ios') 
getfacts(arista,'arista ','eos')       
        
    

    

