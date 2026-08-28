import getpass
# Requires: pip install telnetlib-313-and-up
import telnetlib 
import time

HOST = "192.168.184.141"
user = input("Enter your username: ")
password = getpass.getpass()

# Add a timeout so it doesn't block forever if network drops
tn = telnetlib.Telnet(HOST, timeout=5)

tn.read_until(b"username: ", timeout=5)
tn.write(user.encode('ascii') + b"\r\n")

if password:
    tn.read_until(b"Password: ", timeout=5)
    tn.write(password.encode('ascii') + b"\r\n")

# Give the device a brief moment to stabilize after login
time.sleep(1)

# Send configuration and commands using standard carriage return/newline
tn.write(b"term length 0\r\n")
tn.write(b"show ver\r\n")
tn.write(b"show ip int brie\r\n")
tn.write(b"show ip route\r\n")
tn.write(b"exit\r\n")

# Read until the connection closes or grab available output safely
# Instead of read_all(), use read_very_eager() or read_until a prompt/timeout
output = tn.read_all()
print(output.decode('ascii', errors='ignore'))


