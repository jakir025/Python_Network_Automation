import time
import datetime
import schedule
from getpass import getpass
import paramiko

# 1. Ask for credentials ONCE cleanly when launching the script
USERNAME = 'jakir'
PASSWORD = getpass('Enter device password: ')

def BACKUP():
    # Safe date format for filenames (e.g., 20260905-074500)
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    print(f"\n--- Starting Scheduled Backup Run at {TIMESTAMP} ---")

    # Open the file inside the function so it reads the list fresh each time
    try:
        with open('09_devices_strip', 'r') as file:
            DEVICE_LIST = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("❌ Error: '09_devices_strip' file not found.")
        return

    for RTR in DEVICE_LIST:
        print(f'\n### Connecting to device {RTR} ###')
        
        SESSION = paramiko.SSHClient()
        SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            SESSION.connect(RTR, port=22,
                            username=USERNAME,
                            password=PASSWORD,
                            look_for_keys=False,
                            allow_agent=False,
                            timeout=10)

            DEVICE_ACCESS = SESSION.invoke_shell()
            DEVICE_ACCESS.send(b'term length 0\n')
            time.sleep(1) # Let the prompt stabilize
            DEVICE_ACCESS.send(b'show run\n')
            
            # Wait for data to start generating, then clear out the echo/command intro
            time.sleep(3) 
            
            # Loop to receive the ENTIRE 'show run' output until it finishes printing
            output = ""
            while True:
                if DEVICE_ACCESS.recv_ready():
                    chunk = DEVICE_ACCESS.recv(65535).decode('utf-8', errors='ignore')
                    output += chunk
                    # If we see the hostname prompt again at the end, output is finished
                    if output.strip().endswith("#"):
                        break
                else:
                    # Brief pause to wait for slower network packages
                    time.sleep(1)
                    if not DEVICE_ACCESS.recv_ready():
                        break

            # Save the backup with a safe, unique filename per run
            filename = f'ROUTER_{RTR}_{TIMESTAMP}.txt'
            with open(filename, 'w') as SAVE_FILE:
                SAVE_FILE.write(output)
                
            print(f"✅ Successfully backed up {RTR} to {filename}")
            
        except Exception as e:
            print(f"❌ Error connecting to {RTR}: {e}")
            
        finally:
            SESSION.close()

# Schedule to run every minute at the 00-second mark
schedule.every().minute.at(":00").do(BACKUP)

print("⏰ Backup scheduler successfully started. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(1)

    
