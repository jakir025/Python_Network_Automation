import paramiko
import time
from getpass import getpass
import datetime
TNOW = datetime.datetime.now().replace(microsecond=0)

username = 'jakir'
password = 'Hoss1234'
scp_pass = getpass( prompt = 'Enter scp server password :' )

# Open the file using a context manager ('with') to ensure proper file closing
with open('09_devices_strip', 'r') as file:
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

        DEVICE_ACCESS=SESSION.invoke_shell()
        DEVICE_ACCESS.send('copy nvram:startup-config scp://hoss@192.168.184.135//home/hoss/Documents/ROUTER_' + RTR +'\n\n\n\n')
        time.sleep(5)
        DEVICE_ACCESS.send(scp_pass +'\n')
    
        # Give the device time to process and output the command results
        time.sleep(5)
        
      
        print('Backup Completed !' + RTR + '\n\n')
       

        
    except Exception as e:
        print(f"❌ Error connecting to {RTR}: {e}")
        
    finally:
        # 🌟 Corrected typo: added parentheses to actually execute the close method
        SESSION.close()
