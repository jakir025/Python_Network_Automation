from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

with open('15_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

with open('15_config') as f:
    config_lines = f.read().splitlines()

for ip in ip_list:
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }
    print(f'Connecting to {ip}...')
    try:
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_set(config_lines)
            print(output)

            output = net_connect.send_command('show ip int brief')
            print(output)
    except NetmikoAuthenticationException:
        print(f'  Auth failed on {ip}, skipping.')
    except NetmikoTimeoutException:
        print(f'  Timed out connecting to {ip}, skipping.')
    except Exception as e:
        print(f'  Unexpected error on {ip}: {e}')
