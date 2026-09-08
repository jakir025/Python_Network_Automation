from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

with open('24_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

for ip in ip_list:
    RTR = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }
    print('\nConnecting to the device ' + ip)
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

    # Get output parsed into dict format using TextFSM
    output = net_connect.send_command('show ip int brief', use_textfsm=True)

    # Rename keys: 'interface' -> 'intf', 'ip_address' -> 'ipaddr'
    renamed_output = [
        {
            'intf': row.get('interface'),
            'ipaddr': row.get('ip_address'),
            'status': row.get('status'),
            'proto': row.get('proto'),
        }
        for row in output
    ]

    print(f"--- Output from {ip} ---")
    print(renamed_output)

    # Only the names of up interfaces, no IP/status/proto
    up_interface_names = [row['intf'] for row in renamed_output if row.get('status', '').lower() == 'up']

    print(f"--- Up Interface Names on {ip} ---")
    print(up_interface_names)

    print('\nLIST OF INTERFACES WHICH ARE UP \n#################')
    statusup = [i['interface'] for i in output if i['status'] == 'up']
    for ifaceup in statusup:
        print(ifaceup)
        
    print('\nLIST OF INTERFACES WHICH ARE DOWN \n#################')
    statusdown = [i['interface'] for i in output if i['status'] != 'up']
    for ifacedown in statusdown:
        print(ifacedown)        

    net_connect.disconnect()
