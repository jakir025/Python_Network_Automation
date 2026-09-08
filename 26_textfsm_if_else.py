from netmiko import ConnectHandler
from getpass import getpass
from operator import itemgetter
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

with open('24_devices') as f:
    ip_list = [line.strip() for line in f if line.strip()]

# Change this to whichever index you want to check (0 = first interface)
index_to_check = 1

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
            status = interface_row.get('status')
            print(f"  Intf: {name} | Status: {status}")

        # --- Check a specific interface by index number ---
        if index_to_check < total_interfaces:
            target_interface = output[index_to_check]
            getintf = itemgetter('interface')
            getstatus = itemgetter('status')
            extracted_name = getintf(target_interface)
            extracted_status = getstatus(target_interface)

            print(f'\n Interface at index {index_to_check} -> {extracted_name} status is {extracted_status}')

            # If that interface is down, bring it up with no shutdown
            print("Making backup interface UP")
            if extracted_status in ['down', 'administratively down']:
                print(f'  Interface {extracted_name} is down, sending no shutdown...')
                config_commands = [
                    f'interface {extracted_name}',
                    'no shutdown'
                ]
                config_output = net_connect.send_config_set(config_commands)
                print(config_output)
            else:
                print(f'  Interface {extracted_name} is already up, no action needed.')
        else:
            print(f'\n ⚠️ Index {index_to_check} does not exist (only {total_interfaces} interfaces found).')

    else:
        print("  ⚠️ No interface data parsed by TextFSM.")

    net_connect.disconnect()
