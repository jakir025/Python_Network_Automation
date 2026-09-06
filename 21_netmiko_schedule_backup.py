import time
import datetime
import schedule
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException # Fixed missing import

# 1. Ask for credentials ONCE before entering the automated loop
USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

def BACKUP():
    # Format timestamp to omit file-system breaking colons (e.g., 20260905-061500)
    #TNOW = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    TNOW = datetime.datetime.now().replace(microsecond=0)

    try:
        with open('17_devices') as f:
            ip_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: The '17_devices' file was not found.")
        return

    for IP in ip_list:
        RTR = {
            'device_type': 'cisco_ios',
            'ip': IP,
            'username': USERNAME, # Fixed casing mismatch
            'password': PASSWORD, # Fixed casing mismatch
        }

        print(f'Connecting to the device {IP}...')

        try:
            net_connect = ConnectHandler(**RTR)
            
            print('Initiating config backup at ' + str(TNOW))
            #print(f'Initiating config backup for {IP}...')
            output = net_connect.send_command('show run')
            
            # Using context manager 'with' automatically handles closing files cleanly
            filename = f'ROUTER_{IP}_{TNOW}.txt'
            with open(filename, 'w') as SAVE_FILE:
                SAVE_FILE.write(output)
            
            #print(f'Finished config backup for {IP}.\n')
            #print('Finished config backup at ' + str(TNOW))
            print('Finished config backup')
            
            # Disconnect as soon as you finish interacting with the current device
            net_connect.disconnect()

        except NetmikoAuthenticationException:
            print(f'  Auth failed on {IP}, skipping.\n')
            continue
        except NetmikoTimeoutException:
            print(f'  Device not reachable: {IP}, skipping.\n')
            continue
        except SSHException:
            print(f'  Make sure SSH is enabled on {IP}, skipping.\n')
            continue
        except Exception as e:
            print(f'  Unexpected error connecting to {IP}: {e}\n')
            continue

# Schedule to run every minute at the 00-second mark
schedule.every().minute.at(":00").do(BACKUP)

print("Backup scheduler started. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(1)
    
    
    
    
