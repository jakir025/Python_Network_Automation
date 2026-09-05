from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import time
import datetime
TNOW = datetime.datetime.now().replace(microsecond=0)


with open('20_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

for IP in ip_list:
    RTR = {
        'device_type': 'cisco_ios',
        'ip': IP,
        'username': 'admin1',
        'use_keys': True,
        'key_file': '/home/hoss/PYTHON_DEMO/SSH_KEY/key'
    }

    print('Connecting to the device ' + IP)

    try:
        net_connect = ConnectHandler(**RTR)
    except NetmikoAuthenticationException:
        print(f'  Auth failed on {IP}, skipping.')
        continue
    except NetmikoTimeoutException:
        print(f'  Device not reachable: {IP}, skipping.')
        continue
    except SSHException:
        print('Make sure SSH is enabled')
        continue
    except Exception as e:
        print(f'  Unexpected error connecting to {IP}: {e}')
        continue

    print('\n Initiating config backup \n')
    output = net_connect.send_command('show run')
    print(output)
    SAVE_FILE=open('ROUTER_' + IP + str(TNOW) , 'w' )
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print('\n Finished config backup \n')
    net_connect.disconnect()
