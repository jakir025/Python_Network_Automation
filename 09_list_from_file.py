import paramiko
import time
from getpass import getpass

username = 'jakir'
password = 'Hoss1234'

# Open the file using a context manager ('with') to ensure proper file closing
with open('09_devices', 'r') as file:
    # Use .strip() to clean whitespace and newlines from each host
    DEVICE_LIST = [line.strip() for line in file if line.strip()]

for RTR in DEVICE_LIST:
    # RTR is now clean (e.g., '192.168.1.1' instead of '192.168.1.1\n')
    print('\n ### Connecting to device ' + RTR + ' ###\n')
    
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        SESSION.connect(RTR, port=22,
                        username=username,
                        password=password,
                        look_for_keys=False,
                        allow_agent=False,
                        timeout=10) # Added a timeout so the script doesn't hang indefinitely
        
        DEVICE_ACCESS = SESSION.invoke_shell()
        
        # Initial wait for the device prompt to load
        time.sleep(1)
        
        DEVICE_ACCESS.send(b'config t\n')
        time.sleep(0.5)
        
        for N in range(2, 5):
            DEVICE_ACCESS.send(f'interface loopback {N}\n')
            # 🌟 Added a space before the subnet mask so Cisco accepts it
            DEVICE_ACCESS.send(f'ip address 1.1.1.{N} 255.255.255.255\n')
            time.sleep(0.5)
            
        time.sleep(1)
        DEVICE_ACCESS.send(b'do term length 0\n')
        # 🌟 Added the missing '\n' to execute the command
        DEVICE_ACCESS.send(b'do show ip int brief\n') 
        DEVICE_ACCESS.send(b'end\n')
        DEVICE_ACCESS.send(b'copy running-config startup-config\n')
        DEVICE_ACCESS.send(b'startup-config\n')
        
        # Give the device time to process and output the command results
        time.sleep(3)
        
        output = DEVICE_ACCESS.recv(65000)
        print(output.decode('ascii'))
        
    except Exception as e:
        print(f"❌ Error connecting to {RTR}: {e}")
        
    finally:
        # 🌟 Corrected typo: added parentheses to actually execute the close method
        SESSION.close()

    