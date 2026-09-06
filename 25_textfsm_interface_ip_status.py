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

    # Use TextFSM to parse into a list of dictionaries
    output = net_connect.send_command('show ip int brief', use_textfsm=True)
    
    total_interfaces = len(output)
    print(f'Total number of discovered interfaces: {total_interfaces}')
    
    if total_interfaces > 0:
        up_count = 0
        down_count = 0
        
        # BLOCK 1: Display UP Interfaces
        print("\n--- Active (UP) Interfaces ---")
        for interface_row in output:
            status = interface_row.get('status')
            if status == 'up':
                name = interface_row.get('interface')
                ip_addr = interface_row.get('ip_address')
                proto = interface_row.get('proto')
                print(f"  🟢 {name:<20} | IP: {ip_addr:<15} | Status: {status}/{proto}")
                up_count += 1
                
        # BLOCK 2: Display DOWN Interfaces (Including Administratively Down)
        print("\n--- Inactive (DOWN) Interfaces ---")
        for interface_row in output:
            status = interface_row.get('status')
            # Fixed condition: checks for both standard down and admin down scenarios
            if status in ['down', 'administratively down']:
                name = interface_row.get('interface')
                ip_addr = interface_row.get('ip_address')
                proto = interface_row.get('proto')
                print(f"  🔴 {name:<20} | IP: {ip_addr:<15} | Status: {status}/{proto}")
                down_count += 1
                
        # Consolidated Summary
        print(f"\n📈 Summary Metrics for {ip}:")
        print(f"  Operational (UP):       {up_count}")
        print(f"  Non-Operational (DOWN): {down_count}")
        print(f"  Total Processed:        {total_interfaces}")
    else:
        print("  ⚠️ No interface data parsed by TextFSM.")
    
    net_connect.disconnect()

