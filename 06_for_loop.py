import paramiko
import time
from getpass import getpass
# ip = input('Enter IP:')
# username = input('Enter username:')
# password = input('Enter password:')
ip = '192.168.XXX.XX'
username = 'XXXXX'
password = 'XXXXX'
a = int (input ('Enter first loopback in range : '))
b = int (input ('Enter last loopback in range : ')) + 1
SESSION = paramiko.SSHClient()
SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SESSION.connect(ip,port=22,
                username=username,
                password=password,
                look_for_keys=False,
                allow_agent=False)

DEVICE_ACCESS = SESSION.invoke_shell()
DEVICE_ACCESS.send(b'config t\n')
#for N in range(1,10):
for N in range(a,b):    
    # DEVICE_ACCESS.send('int lo ' +str(N) + '\n')
    # DEVICE_ACCESS.send('ip address 1.1.1.' +str(N) +' 255.255.255.255\n')
############To Remove All Loopback IPs###########
    DEVICE_ACCESS.send('no int lo ' +str(N) + '\n')

time.sleep(5)
DEVICE_ACCESS.send(b'do term length 0\n')
#DEVICE_ACCESS.send(b'show run\n')
DEVICE_ACCESS.send(b'do show ip int brie\n')
DEVICE_ACCESS.send(b'interface FastEthernet0/1\n')
DEVICE_ACCESS.send(b'no shutdown\n')
DEVICE_ACCESS.send(b'end\n')
DEVICE_ACCESS.send(b'copy running-config startup-config\n')
DEVICE_ACCESS.send(b'startup-config\n')
time.sleep(5)
output = DEVICE_ACCESS.recv(65000)
print (output.decode('ascii'))
SESSION.close
