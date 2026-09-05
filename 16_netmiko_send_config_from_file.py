from netmiko import ConnectHandler
from getpass import getpass

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

with open('15_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

with open('15_config') as f:
    config_lines = f.read().splitlines()

for ip in ip_list:
    RTR = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }

    print('Connecting to the device ' + ip)
    net_connect = ConnectHandler(**RTR)

    # output = net_connect.send_config_set(config_lines)
    # print(output)

    output = net_connect.send_config_from_file=('15_config')
    print(output)

    print('\n Saving the configuration \n')
    output = net_connect.save_config()
    print(output)

    output = net_connect.send_command('show ip int brief')
    print(output)

    net_connect.disconnect()