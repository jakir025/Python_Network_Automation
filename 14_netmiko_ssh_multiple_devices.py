from netmiko import ConnectHandler
from getpass import getpass



# 2. Used getpass() so you don't hardcode sensitive passwords
RTR_141 = {
    'device_type': 'cisco_ios',
    'ip':        '192.168.184.141',
    'username':    'jakir',
    'password':  'Hoss1234',
}
RTR_142 = {
    'device_type': 'cisco_ios',
    'ip':        '192.168.184.142',
    'username':    'jakir',
    'password':  'Hoss1234',
}

DEVICE_LIST = [RTR_141,RTR_142]
for DEVICE in DEVICE_LIST:
    print ('Connecting to the device ' + DEVICE['ip'])
    net_connect = ConnectHandler(**DEVICE)

    config_commands = [ 'interface loopback0',
                        'ip address 111.111.111.111 255.255.255.255',
                        'no shutdown']



    output = net_connect.send_config_set(config_commands)
    print(output)

    output = net_connect.send_command('show ip int brief')
    print(output)
