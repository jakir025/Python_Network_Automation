from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

with open('17_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

for ip in ip_list:
    RTR = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }

    print('Connecting to the device ' + ip)

    try:
        net_connect = ConnectHandler(**RTR)
    except NetmikoAuthenticationException:
        print(f'  Auth failed on {ip}, skipping.')
        continue
    except NetmikoTimeoutException:
        print(f'  Device not reachable: {ip}, skipping.')
        continue
    except Exception as e:
        print(f'  Unexpected error connecting to {ip}: {e}')
        continue

    output = net_connect.send_config_from_file('15_config')
    print(output)

    print('\nSaving the configuration\n')
    output = net_connect.save_config()
    print(output)

    output = net_connect.send_command('show ip int brief')
    print(output)

    net_connect.disconnect()