import paramiko
import time
from getpass import getpass


username = 'jakir'
password = 'Hoss1234'

for R in range(141,143):
	ip = '192.168.184.' + str(R)
	print ('\n #### Connecting to the device ' + ip + '###\n')
	SESSION = paramiko.SSHClient()
	SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	SESSION.connect(ip,port=22,
		        username=username,
		        password=password,
		        look_for_keys=False,
		        allow_agent=False)

	DEVICE_ACCESS = SESSION.invoke_shell()
	DEVICE_ACCESS.send(b'config t\n')

	for N in range(2,5):    
	    DEVICE_ACCESS.send('int lo ' +str(N) + '\n')
	    DEVICE_ACCESS.send('ip address 1.1.1.' +str(N) +' 255.255.255.255\n')


	time.sleep(5)
	DEVICE_ACCESS.send(b'do term length 0\n')
	#DEVICE_ACCESS.send(b'show run\n')
	DEVICE_ACCESS.send(b'do show ip int brie\n')
	DEVICE_ACCESS.send(b'end\n')
	DEVICE_ACCESS.send(b'copy running-config startup-config\n')
	DEVICE_ACCESS.send(b'startup-config\n')
	time.sleep(5)
	output = DEVICE_ACCESS.recv(65000)
	print (output.decode('ascii'))
	SESSION.close
