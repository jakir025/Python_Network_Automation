from netmiko import ConnectHandler
from getpass import getpass
from operator import itemgetter
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

    # Use TextFSM to parse into a list of dictionaries
    output = net_connect.send_command('show ip int brief', use_textfsm=True)
    
    total_interfaces = len(output)
    print(f'Total number of interfaces are {total_interfaces}')
    
    if total_interfaces > 0:
        print("--- Interface Summary ---")
        for interface_row in output:
            name = interface_row.get('interface')
            ip_addr = interface_row.get('ip_address')
            status = interface_row.get('status')
            print(f"  Intf: {name} | IP: {ip_addr} | Status: {status}")
            
        # --- SAFE ITEMGETTER PRACTICE ---
        # Use index [0] to safely get the first interface row
        first_interface = output[0] 
        
        # Fixed key from 'intf' to 'interface'
        getintf = itemgetter('interface') 
        getstatus = itemgetter('status')
        
        extracted_name = getintf(first_interface)
        extracted_status = getstatus(first_interface)
        
        print(f'\n Interface {extracted_name} status is {extracted_status}')
        
    else:
        print("  ⚠️ No interface data parsed by TextFSM.")
    
    net_connect.disconnect()


