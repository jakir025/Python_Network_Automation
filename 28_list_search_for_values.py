from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')
search_ip = input('Enter the IP to search for: ')

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

    print('\nSEARCH RESULT \n#################')
    ipsearch = [i['interface'] for i in output if i['ip_address'] == search_ip]
    for ifacename in ipsearch:
        print(f'IP Address {search_ip} belongs to interface {ifacename} on device {ip}')

    net_connect.disconnect()
