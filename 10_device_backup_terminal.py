import paramiko
import time
from getpass import getpass
import datetime
TNOW = datetime.datetime.now().replace(microsecond=0)

username = 'jakir'
password = 'Hoss1234'

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
        DEVICE_ACCESS.send(b'term length 0\n')
        DEVICE_ACCESS.send(b'show run\n')
    
        # Give the device time to process and output the command results
        time.sleep(5)
        
        output = DEVICE_ACCESS.recv(65000)
        print(output.decode('ascii'))
        #SAVE_FILE=open('ROUTER_' + RTR + str(TNOW) , 'w' )
        SAVE_FILE=open('ROUTER_' + RTR ,'w' )
        #SAVE_FILE=open('ROUTER_' + RTR ,'a' )
        SAVE_FILE.write(output.decode('ascii'))
        SAVE_FILE.close

        
    except Exception as e:
        print(f"❌ Error connecting to {RTR}: {e}")
        
    finally:
        # 🌟 Corrected typo: added parentheses to actually execute the close method
        SESSION.close()
